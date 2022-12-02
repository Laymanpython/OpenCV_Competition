import os
import zipfile
import random
import json

'''
参数配置
'''
train_parameters = {
    "input_size": [3, 224, 224],  # 输入图片的shape
    "class_dim": 3,  # 分类数
    "src_path": "data/dataset.zip",  # 原始数据集路径
    "target_path": "data/dataset",  # 要解压的路径
    "train_list_path": "data/train.txt",  # train.txt路径
    "eval_list_path": "data/eval.txt",  # eval.txt路径
    "readme_path": "data/readme.json",  # readme.json路径
    "label_dict": {},  # 标签字典
    "num_epochs": 20,  # 训练轮数
    "train_batch_size": 64,  # 训练时每个批次的大小
    "skip_steps": 30,
    "save_steps": 300,
    "learning_strategy": {  # 优化函数相关的配置
        "lr": 0.0001  # 超参数学习率
    },
    "checkpoints": "work/checkpoints"  # 保存的路径

}


def unzip_data(src_path, target_path):
    '''
    解压原始数据集，将src_path路径下的zip包解压至target_path目录下
    '''
    if (not os.path.isdir(target_path + "Chinese Medicine")):
        z = zipfile.ZipFile(src_path, 'r')
        z.extractall(path=target_path)
        z.close()


def get_data_list(target_path, train_list_path, eval_list_path):
    '''
    生成数据列表
    '''
    # 存放所有类别的信息
    class_detail = []
    # 获取所有类别保存的文件夹名称
    data_list_path = target_path + "/train/"
    class_dirs = os.listdir(data_list_path)
    # 总的图像数量
    all_class_images = 0
    # 存放类别标签
    class_label = 0
    # 存放类别数目
    class_dim = 0
    # 存储要写进eval.txt和train.txt中的内容
    trainer_list = []
    eval_list = []
    # 读取每个类别
    for class_dir in class_dirs:
        if class_dir != ".DS_Store":
            class_dim += 1
            # 每个类别的信息
            class_detail_list = {}
            eval_sum = 0
            trainer_sum = 0
            # 统计每个类别有多少张图片
            class_sum = 0
            # 获取类别路径
            path = data_list_path + class_dir
            # 获取所有图片
            img_paths = os.listdir(path)
            for img_path in img_paths:  # 遍历文件夹下的每个图片
                if img_path.split(".")[-1] == "png":
                    name_path = path + '/' + img_path  # 每张图片的路径
                    if class_sum % 8 == 0:  # 每8张图片取一个做验证数据
                        eval_sum += 1  # test_sum为测试数据的数目
                        eval_list.append(name_path + "\t%d" % class_label + "\n")
                    else:
                        trainer_sum += 1
                        trainer_list.append(name_path + "\t%d" % class_label + "\n")  # trainer_sum测试数据的数目
                    class_sum += 1  # 每类图片的数目
                    all_class_images += 1  # 所有类图片的数目
                else:
                    continue
            # 说明的json文件的class_detail数据
            class_detail_list['class_name'] = class_dir  # 类别名称
            class_detail_list['class_label'] = class_label  # 类别标签
            class_detail_list['class_eval_images'] = eval_sum  # 该类数据的测试集数目
            class_detail_list['class_trainer_images'] = trainer_sum  # 该类数据的训练集数目
            class_detail.append(class_detail_list)
            # 初始化标签列表
            train_parameters['label_dict'][str(class_label)] = class_dir
            class_label += 1

            # 初始化分类数
    train_parameters['class_dim'] = class_dim

    # 乱序
    random.shuffle(eval_list)
    with open(eval_list_path, 'a') as f:
        for eval_image in eval_list:
            f.write(eval_image)

    random.shuffle(trainer_list)
    with open(train_list_path, 'a') as f2:
        for train_image in trainer_list:
            f2.write(train_image)

            # 说明的json文件信息
    readjson = {}
    readjson['all_class_name'] = data_list_path  # 文件父目录
    readjson['all_class_images'] = all_class_images
    readjson['class_detail'] = class_detail
    jsons = json.dumps(readjson, sort_keys=True, indent=4, separators=(',', ': '))
    with open(train_parameters['readme_path'], 'w') as f:
        f.write(jsons)
    print('生成数据列表完成！')
