import jieba
import numpy as np

"""
算法设计
第一步：读取评论数据，对评论进行分句。
第二步：查找对分句的情感词，记录积极还是消极，以及位置。
第三步：往情感词前查找程度词，找到就停止搜寻。为程度词设权值，乘以情感值。
第四步：往情感词前查找否定词，找完全部否定词，若数量为奇数，乘以-1，若为偶数，乘以1。
第五步：判断分句结尾是否有感叹号，有叹号则往前寻找情感词，有则相应的情感值+2。
"""


# 打开词典文件，返回列表
def open_dict(Dict='hahah', path=r'/Users/apple888/PycharmProjects/Textming/Sent_Dict/Hownet/'):
    path = path + '%s.txt' % Dict
    dictionary = open(path, 'r', encoding='utf-8')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict


def judgeodd(num):
    if (num % 2) == 0:  #如果双重否定就是肯定，否则就是否定
        return 'even'
    else:
        return 'odd'


# 注意，这里你要修改path路径。
deny_word = open_dict(Dict='否定词', path=r'/home/zhang/project/Textming/')   #否定词
posdict = open_dict(Dict='positive', path=r'/home/zhang/project/Textming/')  # 积极的
negdict = open_dict(Dict='negative', path=r'/home/zhang/project/Textming/')  # 消极的

degree_word = open_dict(Dict='程度级别词语', path=r'/home/zhang/project/Textming/')
mostdict = degree_word[degree_word.index('extreme') + 1: degree_word.index('very')]  # 权重4，即在情感词前乘以4    4个级别范围
verydict = degree_word[degree_word.index('very') + 1: degree_word.index('more')]  # 权重3
moredict = degree_word[degree_word.index('more') + 1: degree_word.index('ish')]  # 权重2
ishdict = degree_word[degree_word.index('ish') + 1: degree_word.index('last')]  # 权重0.5


def get_ploar(dataset):

    segtmp = jieba.lcut(dataset, cut_all=False)  # 把句子进行分词，以列表的形式返回
    print(segtmp)
    sum2 = 0
    i = 0  # 记录扫描到的词的位置
    a = 0  # 记录情感词的位置
    poscount = 0  # 积极词的第一次分值
    poscount2 = 0  # 积极词反转后的分值
    poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
    negcount = 0
    negcount2 = 0
    negcount3 = 0
    for word in segtmp:
        if word in posdict:  # 判断词语是否是积极情感词
            poscount += 1
            c = 0
            for w in segtmp[a:i]:  # 扫描情感词前的程度词
                if w in mostdict:
                    poscount *= 4.0
                elif w in verydict:
                    poscount *= 3.0
                elif w in moredict:
                    poscount *= 2.0
                elif w in ishdict:
                    poscount *= 0.5
                elif w in deny_word:    #如果是否定词，c+1
                    c += 1
            if judgeodd(c) == 'odd':  # 扫描情感词之前的否定词数
                poscount *= -1.0
                poscount2 += poscount
                poscount = 0
                poscount3 = poscount + poscount2 + poscount3
                poscount2 = 0
            else:
                poscount3 = poscount + poscount2 + poscount3
                poscount = 0
            a = i + 1  # 情感词的位置变化，下次找这个情感词和下一个情感词之间

        elif word in negdict:  # 消极情感的分析，与上面一致
            negcount -= 1
            d = 0
            for w in segtmp[a:i]:
                if w in mostdict:
                    negcount *= 4.0
                elif w in verydict:
                    negcount *= 3.0
                elif w in moredict:
                    negcount *= 2.0
                elif w in ishdict:
                    negcount *= 0.5
                elif w in degree_word:
                    d += 1
            if judgeodd(d) == 'odd':
                negcount *= -1.0
                negcount2 += negcount
                negcount = 0
                negcount3 = negcount + negcount2 + negcount3
                negcount2 = 0
            else:
                negcount3 = negcount + negcount2 + negcount3
                negcount = 0
            a = i + 1
        elif word == '！' or word == '!':  ##判断句子是否有感叹号
            for w2 in segtmp[a:i]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                if w2 in posdict:
                    poscount3 += 2
                    break
                elif w2 in negdict:
                    negcount3 -=2
                    break
            a = i + 1

        sum1 = negcount3+poscount3
        negcount3 = 0
        poscount3 = 0
        sum2 += sum1

        i += 1  # 扫描词位置前移

    print(sum2)
    return sum2

def run(data):
    ploar = get_ploar(data)
    if ploar > 0:
        # print('正面')
        return 1
    elif ploar <0:
        # print('负面')
        return -1
    else:
        # print('中性')
        return 0
