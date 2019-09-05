from math import log


'''
    切记，要做的是一个可以多次使用的决策树而不是只能对隐形眼镜使用
'''

def get_train_set():
    '''
        隐形眼镜的数据集有四个特征，而类标签有3个
        特征分别为:年龄(age),prescript（症状）、astigmatic（是否散光）、tearRate（眼泪数量）
        类标签为：硬材质(hard)、软材质(soft)、不适合佩戴隐形眼镜(no lenses)  
    '''
    return_data = []
    with open('data.txt','r+') as f:
        lines = f.readlines()
        for line in lines:
            customer = {}
            if line == '\n':
                continue
            else:
                new_line = line.split('\t')
                new_line[-1] = new_line[-1].replace('\n','')
                return_data.append(new_line)
        features = ['年龄','症状','是否散光','眼泪数量']
        return return_data,features




def calcShannonEnt(dataset):
    number_of_datas = len(dataset)
    shannonent = 0.0
    labels = {}
    #计算当前每个类标签的数量
    for data in dataset:
        current_label = data[-1] #提取当前的类标签
        if current_label not in labels.keys():
            labels[current_label] = 0
        labels[current_label]+=1
        

    #开始计算熵
    for label in labels.keys():
        chance = float(labels[label] / number_of_datas)
        shannonent+=float(chance * log(chance,2))
    #倒置
    shannonent = -shannonent
    return shannonent

def split_dataset(dataset,feature,value):
    '''
        按特征不同的值将数据集进行分割
    '''
    return_dataset = []

    for data in dataset:
        if data[feature] == value:
            cut_data = data[:feature] + data[feature+1:]
            return_dataset.append(cut_data)
    
    return return_dataset


def choose_best_feature(dataset,features):
    '''
        返回的是最好特征的下标
    '''
    best_info_gain = 0.0
    num_features = len(dataset[0]) - 1
    best_feature = -1
    current_shannoent = calcShannonEnt(dataset)

    for i in range(num_features):
        feature_list = [data[i] for data in dataset]
        feature_value = set(feature_list)
        new_shannoent = 0.0
        #开始计算选出最优特征
        for value in feature_value:
            subdataset = split_dataset(dataset,i,value)  #先预划分
            chance = len(subdataset) / len(dataset)
            new_shannoent+=calcShannonEnt(subdataset) * chance

        new_info_gain = current_shannoent - new_shannoent
        #print("第%d的特征的信息增益为%0.3f" %(i,new_info_gain))
        if new_info_gain > best_info_gain:
            best_feature = i
            best_info_gain = new_info_gain
    
    #print("所以最好的特征为%d" %(best_feature))
    return best_feature
    
def get_classlabel(dataset):
    classlabels = {}
    best_classlabel = ''
    count = 0
    for data in dataset:
        if data[-1] not in classlabels.keys():
            classlabels[data[-1]] = 0
            classlabels[data[-1]]+=1
    
    for key in classlabels.keys():
        if classlabels[key] > count:
            count = classlabels[key]
            best_classlabel = key
    
    return best_classlabel


def create_tree(dataset,features):
    '''
        开始创建决策树
    '''
    #进行判断，如果此时数据集的所有类标签都一样则返回类标签
    class_label_list = [data[-1] for data in dataset]
    if class_label_list.count(class_label_list[0]) == len(class_label_list):
        return class_label_list[0]
    #如果特征集为空，那么返回此时数据集中数量最多的类标签
    if len(features) == 0:
        return get_classlabel(dataset)
    #开始选择最优特征
    best_feature_index = choose_best_feature(dataset,features)
    best_feature = features[best_feature_index]

    del(features[best_feature_index]) #删除被选的特征

    tree = {best_feature:{}}
    #开始进行对数据集的划分
    feature_list = [data[best_feature_index] for data in dataset]
    feature_value = set(feature_list)
    for value in feature_value:
        tree[best_feature][value] = create_tree(split_dataset(dataset,best_feature_index,value),features)

    return tree


def main():
    #得到数据和特征
    dataset,features=get_train_set()
    tree = create_tree(dataset,features)
    '''
        晚上将数据可视化，同时将决策树存储
    '''
    print(tree)

main()