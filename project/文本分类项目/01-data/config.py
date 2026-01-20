# 存储路径/数据库配置信息/API的信息等

# 创建类
class Config(object):
    # 初始化路径属性
    def __init__(self):
        # 文件路径
        self.train_datapath = './train.txt'
        self.test_datapath = './test.txt'
        self.dev_datapath = './dev.txt'
        self.class_datapath = './class.txt'


if __name__ == '__main__':
    # 实例化对象
    config = Config()
    # 获取对象属性
    print(config.train_datapath)
    print(config.class_datapath)