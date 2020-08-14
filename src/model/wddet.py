from model import common_2 as common
import torch.nn.functional as F
import torch.nn as nn
import torch

def make_model(args, parent=False):
    return WDDet(args)

class WDDet(nn.Module):
    def __init__(self, args, conv=common.default_conv):
        super(WDDet, self).__init__()

        n_resblocks = args.n_resblocks
        n_feats = args.n_feats
        kernel_size = 3 
        scale = args.scale[0]
        self.scale = scale
        act = nn.LeakyReLU(0.2, True)
        self.sub_mean = common.MeanShift(args.rgb_range)
        self.add_mean = common.MeanShift(args.rgb_range, sign=1)

        # define head module

        # m_head = [conv(args.n_colors, n_feats, 5), act,
        #             conv(n_feats, n_feats, kernel_size), act,
        #                 conv(n_feats, n_feats, kernel_size), act, 
        #                     conv(n_feats, n_feats, kernel_size), act,
        #                         conv(n_feats, n_feats, kernel_size), act, 
        #                             conv(n_feats, n_feats, kernel_size), act,
        #                                 conv(n_feats, n_feats, kernel_size), act, 
        #                                     conv(n_feats, args.n_colors, 1)]


        m_head = [conv(args.n_colors, n_feats, 5), act,
                    common.OAModule(n_feats, kernel_size, bias=True, use_att=False),
                        common.OAModule(n_feats, kernel_size, bias=True, use_att=False), 
                            common.OAModule(n_feats, kernel_size, bias=True, use_att=True), 
                                common.OAModule(n_feats, kernel_size, bias=True, use_att=True), 
                                    common.OAModule(n_feats, kernel_size, bias=True, use_att=True), 
                                        common.OAModule(n_feats, kernel_size, bias=True, use_att=True), 
                                            common.CBAM(n_feats), act, 
                                                conv(n_feats, args.n_colors, kernel_size)]

        # define body module
        self.body_down = nn.Sequential(common.Shuffle_d(scale=2),
                                    conv(args.n_colors*2*2, n_feats, kernel_size))

        m_body = [
            common.OAModule(
                n_feats, kernel_size, use_att=i>=n_resblocks//4*3 ) for i in range(n_resblocks)
        ]
        m_body.append(conv(n_feats, n_feats, kernel_size))

        # define tail module
        body_tail = [
            nn.PixelShuffle(2),
            conv(int(n_feats//2//2), n_feats, kernel_size),
            nn.ReLU(True),
            conv(n_feats, n_feats, kernel_size),
            nn.ReLU(True)
        ]

        m_tail = [
            conv(args.n_colors*3, n_feats, kernel_size),
            # common.CBAM(n_feats),
            nn.ReLU(True),
            conv(n_feats, args.n_colors, kernel_size),
            # common.CBAM(n_feats),
            # nn.ReLU(False),
            # conv(n_feats, args.n_colors, kernel_size)
        ]

        self.head = nn.Sequential(*m_head)
        self.body = nn.Sequential(*m_body)
        self.body_tail = nn.Sequential(*body_tail)

        self.tail = nn.Sequential(*m_tail)

        # self.dynamic_kernel0 = conv(n_feats, 64, 7) # common.pixelConv(n_feats, 32, 25, 5, 3)
        # self.dynamic_kernel1 = conv(n_feats, 64, 5)
        # self.dynamic_kernel2 = conv(n_feats, 64, 3)

        self.dynamic_kernel0 = common.pixelConv(n_feats, 64, 25, 5, 3)
        self.dynamic_kernel1 = common.pixelConv(n_feats, 96, 49, 7, 3)
        self.dynamic_kernel2 = common.pixelConv(n_feats, 64, 9,  3, 3)
        # self.dynamic_kernel3 = common.pixelConv(n_feats, 64, 81, 9, 3)

        self.upsampler = common.bicubic()


    def forward(self, x):
        with torch.no_grad():
            x, pad_high, pad_weight = self.padding(x)
            x = self.upsampler(x, self.scale)
            x = self.sub_mean(x)
            # x = F.interpolate(x, scale_factor=self.scale, mode='bilinear')
        head_path = self.head(x) + x

        body_down = self.body_down(x)
        body_path = self.body(body_down)
        body_tail = self.body_tail(body_path)

        # dynamic_fmap0 = self.dynamic_kernel0(body_tail) * head_path # self.dynamic_kernel0(body_tail, head_path)
        # dynamic_fmap1 = self.dynamic_kernel1(body_tail) * head_path
        # dynamic_fmap2 = self.dynamic_kernel2(body_tail) * head_path

        dynamic_fmap0 = self.dynamic_kernel0(body_tail, head_path)
        dynamic_fmap1 = self.dynamic_kernel1(body_tail, head_path)
        dynamic_fmap2 = self.dynamic_kernel2(body_tail, head_path)
        # dynamic_fmap3 = self.dynamic_kernel3(body_tail, head_path)

        dynamic_fmap = torch.cat((dynamic_fmap0, dynamic_fmap1, dynamic_fmap2), 1)

        dynamic_fmap = self.tail(dynamic_fmap)
        dynamic_fmap = self.add_mean(dynamic_fmap)

        if pad_high:
            dynamic_fmap = dynamic_fmap[:, :, 3: , : ]           # crop the 
        if pad_weight:
            dynamic_fmap = dynamic_fmap[:, :, :, 3: ]

        return dynamic_fmap 

    def load_state_dict(self, state_dict, strict=True):
        own_state = self.state_dict()
        for name, param in state_dict.items():
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') == -1:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))

    def padding(self, x):
        pad_high = False
        pad_weight = False
        if not x.shape[2]%2 == 0:                 # if the high is odd number
            pad = nn.ZeroPad2d((0,0,1,0))         # padding the top border
            x = pad(x)
            pad_high = True
        if not x.shape[3]%2 == 0:                  # if the weight is od number
            pad = nn.ZeroPad2d((1,0,0,0))          # padding the left border
            x = pad(x)
            pad_weight = True
        
        return x,pad_high,pad_weight
        

