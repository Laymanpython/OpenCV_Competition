import paddle


class ConvPool(paddle.nn.Layer):
    '''卷积+池化'''

    def __init__(self,
                 num_channels,
                 num_filters,
                 filter_size,
                 pool_size,
                 pool_stride,
                 groups,
                 conv_stride=1,
                 conv_padding=1,
                 ):
        super(ConvPool, self).__init__()

        for i in range(groups):
            conv2d = self.add_sublayer(  # 添加子层实例
                'bb_%d' % i,
                paddle.nn.Conv2D(  # layer
                    in_channels=num_channels,  # 通道数
                    out_channels=num_filters,  # 卷积核个数
                    kernel_size=filter_size,  # 卷积核大小
                    stride=conv_stride,  # 步长
                    padding=conv_padding,  # padding
                )
            )
            self.add_sublayer(
                'relu%d' % i,
                paddle.nn.ReLU()
            )
            num_channels = num_filters

        self.add_sublayer(
            'Maxpool',
            paddle.nn.MaxPool2D(
                kernel_size=pool_size,  # 池化核大小
                stride=pool_stride  # 池化步长
            )
        )

    def forward(self, inputs):
        x = inputs
        for prefix, sub_layer in self.named_children():
            x = sub_layer(x)
        return x


# 使用上面的ConvPool模块定义VGGNet
class VGGNet(paddle.nn.Layer):

    def __init__(self):
        super(VGGNet, self).__init__()
        # #3:通道数，64：卷积核个数，3:卷积核大小，2:池化核大小，2:池化步长，2:连续卷积个数(每两组之间)
        self.convpool1 = ConvPool(3, 64, 3, 2, 2, 2)
        self.convpool2 = ConvPool(64, 128, 3, 2, 2, 2)
        self.convpool3 = ConvPool(128, 256, 3, 2, 2, 3)
        self.convpool4 = ConvPool(256, 512, 3, 2, 2, 3)
        self.convpool5 = ConvPool(512, 512, 3, 2, 2, 3)
        self.convpool5_shape = 512 * 7 * 7
        self.fc1 = paddle.nn.Linear(self.convpool5_shape, 4096)
        self.fc2 = paddle.nn.Linear(4096, 4096)
        self.fc3 = paddle.nn.Linear(4096, 3)

    def forward(self, inputs, label=None):

        x = self.convpool1(inputs)
        x = self.convpool2(x)
        x = self.convpool3(x)
        x = self.convpool4(x)
        x = self.convpool5(x)
        x = paddle.reshape(x, [-1, 512 * 7 * 7])
        x = self.fc1(x)
        x = self.fc2(x)
        out = self.fc3(x)

        if label is not None:
            acc = paddle.metric.accuracy(input=out, label=label)
            return out, acc
        else:
            return out

        # 实例化模型


model = VGGNet()
model.eval()
# 加载预训练模型参数
model.set_dict(paddle.load("work/checkpoints/save_dir_1500.pdparams"))

# 定义输入数据
input_spec = paddle.static.InputSpec(shape=[None, 3, 224, 224], dtype='float32', name='image')

# ONNX模型导出
paddle.onnx.export(model, 'home', input_spec=[input_spec])
