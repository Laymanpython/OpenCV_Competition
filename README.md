# OpenCV_Competition
2022 OpenCV Core AI
    **本项目由山东大学信息学院20级通信工程专业学生：李鑫、仲浩、李欣竹、王籽予共同开发，指导老师为山东大学信息学院贲睍晔教授和陈雷副教授
    本项目通过使用神经网络和OpenCV训练图像处理模型 ，分别搭建了以VGGNet和UNet为处理模型的分类和分割医学检测模型，项目使用的工具有Pytorch、OpenMMLab、PaddlePaddle，参考的公开项目有：新冠肺炎辅助诊断系统、新冠X-射线图像识别，并将分类代码写为配置文件，移植到MMClassification中。通过导出ONNX文件进行PC端的部署，来实现该软件的各种功能。从理论上对肺炎医学诊疗具有一定的辅助作用。
    
    医学免责声明：本项目未经临床检验，所得到的模型评价指标仅为实验数据集上的结果，任何临床使用的算法需要在实际使用环境下进行实验，本模型结果不可作为临床诊疗依据。**
    
    This project is jointly developed by Xin Li, Hao Zhong, Xinzhu Li, and Ziyu Wang, students majoring in communication engineering in the 20th grade of the School of Information Science and Engineering, Shandong University. The instructors are Professor Xianye Ben and Associate Professor Lei Chen from the School of Information Science and Engineering, Shandong University
    
    
    This project uses neural networks and OpenCV to train image processing models, and builds classification and segmentation medical detection models with VGGNet and UNet as processing models respectively. The tools used in the project are Pytorch,OpenMMLab and PaddlePaddle, and the referenced public projects are: New Coronary Pneumonia Auxiliary Diagnosis system, new crown X-ray image recognition, and the classification code is written as a configuration file and transplanted into MMClassification. Various functions of the software are realized by exporting the ONNX file for deployment on the PC side. In theory, it has a certain auxiliary role in the medical diagnosis and treatment of pneumonia.
    
    
    Medical disclaimer: This project has not been clinically tested, and the obtained model evaluation indicators are only the results of the experimental data set. Any clinically used algorithm needs to be tested in the actual use environment, and the results of this model cannot be used as a basis for clinical diagnosis and treatment.
    

这是Pneumonia Detection Assistant（肺炎检测助手）的代码仓库，在本仓库中，我们更新了软件最终的可执行文件和各部分的代码

项目的主要包括：X光肺炎诊断和CT病灶分割

X光肺炎诊断的实现主要通过VGGNet实现，最终测试集上的准确率答到了96%

VGGNet论文

链接：https://arxiv.org/abs/1409.1556

模型训练参数

链接: https://pan.baidu.com/s/1cZaPMnvVK0nAgNZbSJOLyg 提取码: r5tk 

onnx模型：

链接: https://pan.baidu.com/s/13zCKsrFxVEuo3llD-Ry7XQ 提取码: 4u4d 

x光的部署是通过C#进行的

CT病灶分割中

模型使用BiSeNetv2

论文介绍参考：https://zhuanlan.zhihu.com/p/141692672

由于网上关于C#进行分割模型部署的资料比较少。所以我们选取了通过pyqt设计页面，将最终的文件打包为exe可执行文件

然后通过C#进行命令行的调用
