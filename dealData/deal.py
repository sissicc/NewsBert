import os
import logging as log
import pandas as pd
import pickle
import time
import re

# 获取文本文件的路径
def getFilePathList(rootDirPath):
    filePath_list = []
    for walk in os.walk(rootDirPath):
        part_filePath_list = [os.path.join(walk[0], file) for file in walk[2]]
        filePath_list.extend(part_filePath_list)
    return filePath_list

# 获取不重复标签List
def getLables(rootDirPath):
    lableList =[]
    for path in os.listdir(rootDirPath):
        lableList.append(path.split('\\')[-1])
    return lableList


# # 获取所有的样本标签
# def getLables(filePathList):
#     lable_list = []
#     for filePath in filePathList:
#         lable = filePath.split("\\")[-2]
#         lable_list.append(lable)
#     return lable_list

# 保存文件为pickle格式，
def dumpListPickle(fileName,list):
    with open(fileName,'wb') as file:
        pickle.dump(list,file)

# 获取文件内容
def getFileContext(filePath):
    with open(filePath,encoding='utf8') as file:
        label = filePath.split('\\')[-2]
        title = re.sub('\s+',' ',file.readline(1000))
        context =re.sub('s+',' ',file.read())
    return label,title,context

# 获取样本内容，保存content_list
def saveContent_list(file_path_list,label_list):
    interval = 20000
    n_samples = len(label_list)
    startTime = time.time()
    directory_name='context_list'
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)
    for i in range(0,n_samples,interval):
        startIndex = i
        endIndex = i+interval
        context_list =[]
        print('%06d-%06d' %(startIndex,endIndex))
        for filePath in file_path_list[startIndex:endIndex]:
            fileStr= getFileContext(filePath)
            context = re.sub('\s+',' ',fileStr)
            context_list.append(context)
            save_fileName = directory_name+'/%06d-%06d.pickle' %(startIndex,endIndex)
        dumpListPickle(save_fileName,context_list)
        used_time = time.time() -startTime
        print('%06d-%06d used time: %.2f seconds' %(startIndex,endIndex,used_time))

def saveLable2Context(filePathList,labelList):
    interval = 20000
    midInterval =10000
    n_samples = len(labelList)
    startTime = time.time()
#    directory_name = 'label2Context'
    train_data_dir_name='data/train'
    dev_data_dir_name='data/dev'
    test_data_dir_name='data/test'
    for i in range(0, n_samples, interval):
        startIndex = i
        endIndex = i + interval
        label2Context_list = []
        print('%06d-%06d' % (startIndex, endIndex))
        mid =i+midInterval;
        for filePath in filePathList[startIndex:mid]:
            fileStr = getFileContext(filePath)
            label2Context_list.append('\t'.join(fileStr)+'\n' )
        if (endIndex % 50000 == 0):  # 验证集和测试集
            dev_fileName = dev_data_dir_name+'/%06d-%06d.pickle' % (startIndex,mid)
            dumpListPickle(dev_fileName,label2Context_list)
            label2Context_list = []# 测试集
            for filePath in filePathList[mid:endIndex]:
                fileStr = getFileContext(filePath)
                label2Context_list.append('\t'.join(fileStr) + '\n')
            test_fileName =test_data_dir_name+'/%06d-%06d.pickle' %(mid,endIndex)
            dumpListPickle(test_fileName,label2Context_list)
        else:
            for filePath in filePathList[mid:endIndex]:
                fileStr = getFileContext(filePath)
                label2Context_list.append('\t'.join(fileStr)+'\n')
            train_fileName = train_data_dir_name + '/%06d-%06d.pickle' % (startIndex, endIndex)
            dumpListPickle(train_fileName, label2Context_list)
        used_time = time.time() - startTime
        print('%06d-%06d used time: %.2f seconds' % (startIndex, endIndex, used_time))



# 加载pickle文件
def loadPickle(fileName):
    with open(fileName,'rb') as file:
        label_list=(pickle.load(file))
    return label_list


def _load_path(fileDir):
    file_path_list =[]
    file_path_list = getFilePathList(fileDir)
    lableTitleContextList =[]
    for filePath in file_path_list:
        context = loadPickle(filePath)
        lableTitleContextList.append(context)
    return lableTitleContextList


if __name__ == '__main__':
    dir = 'D:\mygit\lw\code\data\THUCNews\THUCNews'
    lableList =getLables(dir);
 #   start = time.time()
 #   file_path_list = getFilePathList(dir)
 #   end1 = time.time()
#    l = len(file_path_list)
 #   print('获取文本路径共：%d 条，花费时间：%.2f seconds' %(l,end1-start))

    # # print(l)
    # start2 = time.time()
    # label_list = getLables(file_path_list)
    # result =pd.value_counts(label_list)
    # end2 = time.time()
    # print('获取文本标签：花费时间：%.2f seconds'%(end2-start2))
    # start3 = time.time()
   # saveContent_list(file_path_list,label_list)
 #   saveLable2Context(file_path_list,label_list)
   # end3 = time.time();
   # print('保存所有样本内容，保存context_list，花费时间：%.2f' %(end3-start3))
    # print(result)
    # fileName ='label_list.pickle'
    # dumpLabels(fileName,label_list)
    # labels = loabLable(fileName)
    # res = pd.value_counts(labels)
    #print(res)
    # data_root ="C:\\Users\csdc\PycharmProjects\dealData\data"
#     # type = 'test'
#     # contextList=_load_path(data_root+'/'+type)
#     # for context in contextList:
#     #     for (i,c) in enumerate(context):
#     #         guid = '%s-%s' % (type, i)
#     #         cont = re.split('\t', c)
#     #         label = cont[0]
#     #         text = cont[2]
            # print(label)



