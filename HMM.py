import pickle
import math
'''
    train-test=[]
    wordID-tagID-Id2tag-Id2word={}
    numberWord-numberTag=[]
    A-B={}
'''
A=pickle.load(open("A.pkl","rb"))
B=pickle.load(open("B.pkl","rb"))
wordId=pickle.load(open("wordId.pkl","rb"))
tagId=pickle.load(open("tagId.pkl","rb"))
Id2word=pickle.load(open("Id2word.pkl","rb"))
Id2tag=pickle.load(open("Id2tag.pkl","rb"))
#train=pickle.load(open("train.pkl","rb"))
test=pickle.load(open("test.pkl","rb"))
PI=pickle.load(open("PI.pkl","rb"))
sum=pickle.load(open("sum.pkl","rb"))
numberTag=pickle.load(open("numberTag.pkl","rb"))
numberTagB=pickle.load(open("numberTagB.pkl", "rb"))

sum+=1
alltag=len(tagId)
gaptag = 10000000
fw=open("testlable.txt","w")
def viterbi(sentence,label):
    delta=[]#计算delta矩阵
    path=[]#计算回溯矩阵
    for epoch in range(len(sentence)):
        deltares = []
        pathres = []
        if epoch==0:#计算第一列
            for tag in range(alltag):
                if B.get(tag*gaptag+sentence[epoch]) is None:#如果是训练集不存在这个
                    deltares.append(math.log2(PI[tag])+math.log2(1/(numberTagB[int(tag/gaptag)]+len(wordId))))#平滑一下
                else :#如果训练集存在的话
                    deltares.append(math.log2(PI[tag]) + math.log2(B[tag*gaptag+sentence[epoch]]))#PI与当前的发射概率相乘。log之后就是相加了
                pathres.append(-1)#添加结束符
            delta.append(deltares)
            path.append(pathres)
        else :#不是第一行，使用viterbi
            for tagi in range(alltag):
                MX = -1000000#当前的最优值
                MXJ=-1#当前的最优下标
                for tagj in range(alltag):
                    if A.get(tagj*gaptag+tagi) is None:#状态矩阵中不存在这样的转移
                        nowdel = delta[-1][tagj] + math.log2(1/(numberTag[tagj]+1))#平滑一下
                    else :#存在就正常计算
                        nowdel=delta[-1][tagj]+math.log2(A[tagj*gaptag+tagi])
                    if nowdel>MX:#发现更优解
                        MX=nowdel
                        MXJ=tagj
                if B.get(tagi * gaptag + sentence[epoch]) is None:#当前的观察矩阵不存在这样的发射概率，平滑一下
                    deltares.append(MX + math.log2(1 / (numberTagB[tagi] + len(wordId))))
                else :#当前的观察矩阵存在这样的发射概率，正常计算
                    deltares.append(MX + math.log2(B[tagi * gaptag + sentence[epoch]]))
                pathres.append(MXJ)
            delta.append(deltares)#保存结果
            path.append(pathres)
    MX=-1000000
    MXI=0
    for i in range(alltag):#找最后的最优结果
        if delta[-1][i]>MX:
            MX=delta[-1][i]
            MXI=i
    cnt=-1
    ans=[]
    while MXI!=-1:#回溯最优解
        ans.append(MXI)
        MXI =path[cnt][MXI]
        cnt-=1
    ans.reverse()
    ret=0
    #print(ans,"\n",label)
    for i in range(len(ans)):#计算一下当前的正确的个数
        fw.write(str(Id2word[sentence[i]])+"\t"+str(Id2tag[label[i]])+"\t"+str(Id2tag[ans[i]])+"\n")
        if ans[i]==label[i]:
            ret+=1
    print(ret,len(ans))
    return ret
def predict():
    fw.write("word\tlable\tpredictlabel\n")
    all=0
    cnt=0
    sentence=[]
    label=[]
    for word in test:
        if word[0]!=-1:#得到句子
            sentence.append(word[0])
            label.append(word[1])
        else :#开始预测
            all += len(sentence)  # 句子多长
            cnt+=viterbi(sentence,label)#使用viterbi计算对了多少个
            sentence=[]
            label=[]
            fw.write("\n")
    fw.close()
    print(cnt/all)#输出结果
if __name__ == '__main__':
    predict()
