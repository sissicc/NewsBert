import os
import logging as log
import pandas as pd
import pickle
import time
import re

# 数据量太大，bert跑会oom

# 获取文本文件的路径
def getRootPathList(rootDirPath):
    dirPathList = []
    for path in os.listdir(rootDirPath):
        dirPathList.append(os.path.join(rootDirPath,path))
    return dirPathList

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

def saveLable2Context(dirPathList):
    interval = 2000
    midInterval =1000
    train_samples = 10000;
    startTime = time.time()
#    directory_name = 'label2Context'
    train_data_dir_name='../nData/train'
    dev_data_dir_name='../nData/dev'
    test_data_dir_name='../nData/test'
    for dirIndex,dir in  enumerate(dirPathList):
        filePathList =[]
        filePathList = getRootPathList(dir)
        for i in range(0, train_samples, interval):
            startIndex = i
            endIndex = i + interval
            midIndex = startIndex+midInterval
            label2Context_list = []
            print('%06d-%06d' % (startIndex, endIndex))
            for filePath in filePathList[startIndex:midIndex]:
                fileStr = getFileContext(filePath)
                label = fileStr[0]
                label2Context_list.append('\t'.join(fileStr)+'\n' )
            if (endIndex % 5000 == 0):  # 验证集和测试集
                dev_fileName = dev_data_dir_name+'/%02d%06d-%06d.pickle' % (dirIndex,startIndex,midIndex)
                dumpListPickle(dev_fileName,label2Context_list)
                print("save pickle :%s"%dev_fileName)
                label2Context_list = []# 测试集
                for filePath in filePathList[midIndex:endIndex]:
                    fileStr = getFileContext(filePath)
                    label2Context_list.append('\t'.join(fileStr) + '\n')
                test_fileName =test_data_dir_name+'/%2d%06d-%06d.pickle' %(dirIndex,midIndex,endIndex)
                dumpListPickle(test_fileName,label2Context_list)
                print("save pickle :%s" % test_fileName)
            else:
                for filePath in filePathList[midIndex:endIndex]:
                    fileStr = getFileContext(filePath)
                label2Context_list.append('\t'.join(fileStr)+'\n')
                train_fileName = train_data_dir_name + '/%02d%06d-%06d.pickle' %(dirIndex,startIndex, endIndex)
                dumpListPickle(train_fileName, label2Context_list)
                print("save pickle :%s " %train_fileName)
        used_time = time.time() - startTime
        print('%06d-%06d used time: %.2f seconds' % (startIndex, endIndex, used_time))



# 加载pickle文件
def loadPickle(fileName):
    with open(fileName,'rb') as file:
        label_list=(pickle.load(file))
    return label_list


def _load_path(fileDir):
    file_path_list =[]
    file_path_list = getRootPathList(fileDir)
    lableTitleContextList =[]
    for filePath in file_path_list:
        context = loadPickle(filePath)
        lableTitleContextList.append(context)
    return lableTitleContextList


if __name__ == '__main__':
    dir = 'D:\mygit\lw\code\data\THUCNews\THUCNews'
    start = time.time()
    label_list = getLables(dir)
    end1= time.time()
    print('获取文本标签共：%d 条，花费时间：%.2f seconds' % (len(label_list), end1 - start))
    dir_path_list = getRootPathList(dir)
    end2 = time.time()
    print('获取文本路径共：%d 条，花费时间：%.2f seconds' % (len(dir_path_list),end2-end1))
    saveLable2Context(dir_path_list)
    print('共花费时间：%.2f seconds' % ( time.time()-start))
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



