import paddle
import matplotlib.pyplot as plt
from Dataset import dataset
from model import VGGNet
from data_processing import unzip_data, train_parameters, get_data_list

'''
参数初始化
'''
src_path = train_parameters['src_path']
target_path = train_parameters['target_path']
train_list_path = train_parameters['train_list_path']
eval_list_path = train_parameters['eval_list_path']

'''
解压原始数据到指定路径
'''
unzip_data(src_path, target_path)

'''
划分训练集与验证集，乱序，生成数据列表
'''
# 每次生成数据列表前，首先清空train.txt和eval.txt
with open(train_list_path, 'w') as f:
    f.seek(0)
    f.truncate()
with open(eval_list_path, 'w') as f:
    f.seek(0)
    f.truncate()

# 生成数据列表
get_data_list(target_path, train_list_path, eval_list_path)

train_dataset = dataset('data', mode='train')
train_loader = paddle.io.DataLoader(train_dataset, batch_size=16, shuffle=True)

train_dataset.print_sample(200)
#print(train_dataset.__len__())


def draw_process(title, color, iters, data, label):
    plt.title(title, fontsize=24)
    plt.xlabel("iter", fontsize=20)
    plt.ylabel(label, fontsize=20)
    plt.plot(iters, data, color=color, label=label)
    plt.legend()
    plt.grid()
    plt.show()


model = VGGNet()
model.train()
cross_entropy = paddle.nn.CrossEntropyLoss()
optimizer = paddle.optimizer.Adam(learning_rate=train_parameters['learning_strategy']['lr'],
                                  parameters=model.parameters())

steps = 0
Iters, total_loss, total_acc = [], [], []

for epo in range(train_parameters['num_epochs']):
    for _, data in enumerate(train_loader()):
        steps += 1
        x_data = data[0]
        y_data = data[1]
        predicts, acc = model(x_data, y_data)
        loss = cross_entropy(predicts, y_data)
        loss.backward()
        optimizer.step()
        optimizer.clear_grad()
        if steps % train_parameters["skip_steps"] == 0:
            Iters.append(steps)
            total_loss.append(loss.numpy()[0])
            total_acc.append(acc.numpy()[0])
            # 打印中间过程
            print('epo: {}, step: {}, loss is: {}, acc is: {}' \
                  .format(epo, steps, loss.numpy(), acc.numpy()))
        # 保存模型参数
        if steps % train_parameters["save_steps"] == 0:
            save_path = train_parameters["checkpoints"] + "/" + "save_dir_" + str(steps) + '.pdparams'
            print('save model to: ' + save_path)
            paddle.save(model.state_dict(), save_path)
paddle.save(model.state_dict(), train_parameters["checkpoints"] + "/" + "model_final.pdparams")
draw_process("trainning loss", "red", Iters, total_loss, "trainning loss")
draw_process("trainning acc", "green", Iters, total_acc, "trainning acc")
