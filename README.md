# ThucNewsBert
根据bert对thuc新闻数据集进行文本分类，只需要修改`run_classifer`即可
## 准备
* 下载数据集：[ThucNews](http://thuctc.thunlp.org/)，大小为1.5G
* 下载[`bert源码`](https://github.com/google-research/bert)
* 下载中文预训练模型:[`BERT-Base, Chinese`](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)
## 处理
* 使用Thuc全部数据会OOM，所以只用了部分数据，也可以修改`train_batch_size`
* 根据数据集形式，在`run_classifier`中仿照示例完成`ThucNewsProcess`模块，并加到`processors字典`
* 训练，`run.sh`
