import pickle
import random
if __name__ == '__main__':
    '''
    train-test=[]
    wordID-tagID-Id2tag-Id2word={}
    numberTagB-numberTag=[]
    A-B={}
    '''
    train=[]
    test=[]
    wordId={}
    Id2word={}
    allword=0
    tagId={}
    Id2tag = {}
    alltag=0
    A={}
    B={}
    numberTagB=[]
    numberTag=[]
    PI=[]
    sum=0
    gaptag = 10000000
    with open("raw_data.txt","r",encoding="utf-8") as fr:
        for line in fr:
            line=line.strip().split(" ")
            choose=random.randint(1,20)#随机分测试集和训练集
            pretag=-1#前一个观察序列的值
            res=0
            ok=0
            for word in line :
                word=word.split("/")#分词
                if len(word)==2 :
                    if wordId.get(word[0]) is None:#给观察序列构造字典
                        wordId[word[0]]=allword
                        Id2word[allword]=word[0]
                        allword+=1
                    if tagId.get(word[1]) is None:#给状态序列构造字典
                        tagId[word[1]]=alltag
                        Id2tag[alltag]=word[1]
                        numberTag.append(0)
                        numberTagB.append(0)
                        PI.append(0)
                        alltag+=1
                    word[0]=wordId[word[0]]#下标替换
                    word[1] = tagId[word[1]]#下标替换
                    if choose == 20:#表示进入测试集
                        test.append([word[0],word[1]])
                    else:#表示进入训练集
                        PI[word[1]]+=1
                        sum+=1
                        numberTagB[word[1]] += 1#为了计算B矩阵，我们统计其分母部分
                        numberTag[word[1]] += 1#了计算A矩阵，我们统计其分母部分
                        res=[word[0],word[1]]#最后一个的话，我们需要减掉，因为对A矩阵有影响,注意这里对B没有影响的
                        if pretag>=0:#第一个没法计算，所以这样搞一下
                            if A.get(pretag*gaptag+word[1]) is None :#为了节省空间，进行hash
                                A[pretag*gaptag+word[1]]=0
                            A[pretag*gaptag+word[1]]+=1
                        if B.get(word[1] * gaptag + word[0]) is None:#为了节省空间，进行hash
                            B[word[1] * gaptag + word[0]] = 0
                        B[word[1] * gaptag + word[0]] += 1
                        pretag=word[1]#记录前一个观察序列的标号
                        train.append([word[0], word[1]])
            if choose == 20:
                test.append([-1, -1])#作为句子的结尾
            else :
                numberTag[res[1]] -= 1#减掉影响结果的那一部分
                train.append([-1,-1])
    for i in range(len(PI)):
        PI[i]=(PI[i]+1)/(sum+len(tagId))#对PI进行平滑的搞一下
    for tag in A.keys():
        A[tag]=(A[tag]+1)/(numberTag[int(tag/gaptag)]+len(tagId))#对A进行平滑的搞一下
    for tag in B.keys():
        B[tag]=(B[tag]+1)/(numberTagB[int(tag/gaptag)]+len(wordId))#对B进行平滑的搞一下
    #保存训练好的模型
    pickle.dump(A, open("A.pkl", "wb"))
    pickle.dump(B, open("B.pkl", "wb"))
    pickle.dump(wordId, open("wordId.pkl", "wb"))
    pickle.dump(tagId, open("tagId.pkl", "wb"))
    pickle.dump(Id2word, open("Id2word.pkl", "wb"))
    pickle.dump(Id2tag, open("Id2tag.pkl", "wb"))
    pickle.dump(numberTagB, open("numberTagB.pkl", "wb"))
    pickle.dump(numberTag, open("numberTag.pkl", "wb"))
    pickle.dump(train, open("train.pkl", "wb"))
    pickle.dump(test, open("test.pkl", "wb"))
    pickle.dump(PI, open("PI.pkl", "wb"))
    pickle.dump(sum, open("sum.pkl", "wb"))
'''
B=pickle.load(open("A.pkl","rb"))
print(B)
'''
