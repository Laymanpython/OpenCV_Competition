# 新冠肺炎检测 
项目说明：

数据集：https://aistudio.baidu.com/aistudio/datasetdetail/121203

科研学者们收集并开源的新冠肺炎阳性患者的胸部x线影像数据库（包括正常、病毒性肺、新冠阳性三种影像），旨在通过深度学习建模，准确识别出其中的新冠阳性影像

train.py:训练脚本

test.py:训练脚本

eval.py:评估脚本

model.py:定义网络结构

data_processing.py:解压数据、划分数据集

Dataset.py:继承paddle的dataset,适配本数据集。

onnx_output.py:输出onnx模型

work/checkpoints：存放训练后参数

data/dataset:存放数据集的目录
