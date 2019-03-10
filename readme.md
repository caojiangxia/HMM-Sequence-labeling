# HMM-曹江峡

## 运行方式

首先将raw_data.txt,pre.py,HMM.py置于相同目录下。

之后运行pre.py文件，进行划分训练集train与测试集test，比例为19:1，之后通过极大似然估计得到A,B,wordId,Id2Word,PI,tagId,Id2tag,numberWord,numberTag等参数。程序结束时则将隐马模型构建完毕。

最后运行HMM.py文件，开始使用viterbi前向算法进行预测。生成test文件的预测结果testlabel.txt文件，在程序结束后便于查看预测效果。

运行命令:

python pre.py

python HMM.py

pre.py本机运行时间约3分钟
HMM.py本机运行时间约30分钟，请耐心等待

注意本程序的pre.py有随机部分，故复现结果可能有少许不同，但是准确率稳定在0.90以上。
## 程序的一些trick

为了节省空间与加速查询，A,B矩阵的存储形式为哈希表存储

为了减少viterbi的精度损失，在计算过程中均使用取log方式将乘法转为加法



## 参考书籍

李航-《统计学习方法》
