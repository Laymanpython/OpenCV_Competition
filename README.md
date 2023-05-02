# OpenCV_Competition
2022 OpenCV Core AI


  本项目由山东大学信息学院20级通信工程专业学生：李鑫、仲浩、李欣竹、王籽予共同开发，指导老师为山东大学信息学院翟超副教授、贲晛烨教授和陈雷副教授
  
本项目通过使用神经网络和OpenCV训练图像处理模型 ，分别搭建了以VGGNet和BiSeNet V2为处理模型的分类和分割医学检测模型。参考的公开项目有：新冠肺炎辅助诊断系统、新冠X-射线图像识别。通过导出ONNX文件进行PC端的部署，来实现该软件的各种功能。从理论上对肺炎医学诊疗具有一定的辅助作用。

医学免责声明：本项目未经临床检验，所得到的模型评价指标仅为实验数据集上的结果，任何临床使用的算法需要在实际使用环境下进行实验，本模型结果不可作为临床诊疗依据。

这是Pneumonia Detection Assistant（肺炎检测助手）的代码仓库，在本仓库中，我们更新了软件最终的可执行文件和各部分的代码

   项目的主要模块包括：X光肺炎诊断和CT病灶分割

   X光肺炎诊断的实现主要通过VGGNet实现，最终测试集上的准确率达到了96%

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

   由于网上关于C#进行分割模型部署的资料比较少。所以我们选取了通过pyqt设计页面

   然后通过C#进行命令行的调用


note:

由于github上传文件大小的原因，我们的代码中有一部分package无法上传上去（主要在C#中需要安装onnx推理有关的package），我们将完整的代码放在了百度网盘上


完整的代码和项目展示视频在：链接：https://pan.baidu.com/s/1o_52Dn6GxFULBEgE_sqj0w  提取码：ejyv

