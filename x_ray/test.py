import os
import paddle
import numpy as np
from PIL import Image
from model import VGGNet
from data_processing import train_parameters

# 加载图片函数
def load_image(img_path):
    '''
    预测图片预处理
    '''
    img = Image.open(img_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((224, 224), Image.BILINEAR)
    img = np.array(img).astype('float32')
    img = img.transpose((2, 0, 1)) / 255 # HWC to CHW 及归一化
    return img

# 测试集路径
infer_dst_path = 'data/dataset/test/'
# 标签字典：根据自己的数据处理方式修改此处 ！！！！！！！！！！！
label_dic = train_parameters['label_dict']
# 模型加载：根据自己模型的保存路径，修改此处！！！！！！！！！！！
model__state_dict = paddle.load('work/checkpoints/save_dir_1500.pdparams')
# 模型类：根据自己定义的模型类，没修改此处 ！！！！！！！！！！！
model_predict = VGGNet()


model_predict.set_state_dict(model__state_dict)
model_predict.eval()

infer_imgs_path = os.listdir(infer_dst_path)
infer_imgs_path = [path for path in infer_imgs_path if path!=".DS_Store"]
result_path="data/result.txt"
fout = open(result_path,"w",encoding="utf-8")
for infer_img_path in infer_imgs_path:
    infer_img = load_image(infer_dst_path+infer_img_path)
    infer_img = infer_img[np.newaxis,:, : ,:]  #reshape(-1,3,224,224)
    infer_img = paddle.to_tensor(infer_img)
    result = model_predict(infer_img)
    lab = np.argmax(result.numpy())
    fout.write("{}\t{}\n".format(infer_img_path,label_dic[str(lab)])) # 注意tab符号分隔图片路径与标签类型
    print("样本: {},被预测为:{}".format(infer_img_path,label_dic[str(lab)]))
fout.close()