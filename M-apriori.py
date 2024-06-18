# -*- coding: UTF-8 -*-
import csv
import itertools
import os
import psutil
import time



def findsubsets(S, m):
    return set(itertools.combinations(S, m))


def find_frequent_1_itemsets(D, minSupport,trans):
    L1 = []  # 候选集项Cn生成的频繁项集Lk
    L1_data = []
    L1_sup = []
    fre_L1 = []
    l1=[]
    for key in D:
        L1 = []
        if len(D[key])/trans >= minSupport:
            l1.append(key)
            L1.append(key)
            L1.append(len(D[key]))
            L1.append(D[key])
            fre_L1.append(L1)
    print("----------------------FREQUENT 1-ITEMSET----------------------------------")
    print(l1)
    print("--------------------------------------------------------------------------")
    print()

    return fre_L1


def genSubsets(item):
    subsets = []
    for i in range(1, len(item)):
        subsets.extend(itertools.combinations(item, i))
    return subsets

def has_infrequent_subset(c, Lk_1, k):
    list = []
    list = findsubsets(c, k)
    for item in list:
        s = []
        for l in item:
            s.append(l)
        s.sort()
        if s not in Lk_1:
            return True
    return False

def candidates_from(Lk, k):
    # Lk=[]
    # for item in Lk_1:
    #     Lk.append([item])

    length = k
    Ck = []
    for list1 in Lk:
        for list2 in Lk:
            count = 0
            c = []
            if list1 != list2:
                while count < length - 1:
                    if list1[count] != list2[count]:
                        break
                    else:
                        count += 1
                else:
                    if list1[length - 1] < list2[length - 1]:
                        for item in list1:
                            c.append(item)
                        c.append(list2[length - 1])
                        if not has_infrequent_subset(c, Lk, k):
                            Ck.append(c)
                            c = []
    return Ck


def Get_item_min_sup(Ck, L1):
    x = []
    dic_L1 = {}
    for fre in L1:
        dic_L1[fre[0]] = fre[1]

    item_min_sup = []
    for item in Ck:
        temp_dic = {}
        for ele in item:
            temp_dic[ele] = dic_L1[ele]
        a = zip(temp_dic.values(), temp_dic.keys())
        x.append(min(a)[1])
    return x




def Read_Data(filename, delimiter=','):
    dataset = []
    with open(filename, 'r',encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            dataset.append(row)

    data = {}
    trans = 0
    f = open(filename, 'r', encoding="utf8")
    reader = csv.reader(f)
    for row in reader:
        trans += 1
        for item in row:
            if item not in data:
                data[item] = set()
            data[item].add(trans)
    f.close()
    return dataset, data, trans


def get_Transaction_ID(x, L1):
    dic_L1 = {}
    for fre in L1:
        dic_L1[fre[0]] = fre[2]
    id = []
    for item in x:
        id.append(dic_L1[item])
    return id


def Scan(Tgt, Ck, dataset, sup,trans):
    i = 0
    Lk = {}
    for item in Ck:
        supp = 0
        for id in Tgt[i]:
            if set(item) <= set(dataset[id - 1]):
                supp += 1
        Lk[tuple(item)] = supp

        i += 1

    fre_Lk = []
    for item in Lk:

        if Lk[tuple(item)]/trans >= sup:
            fre_Lk.append(list(item))
    return fre_Lk


def M_Apriori(dataset, data, minsup,trans):
    # 获得1频繁项集
    L1 = find_frequent_1_itemsets(data, minsup,trans)
    L_1 = []
    for item in L1:
        L_1.append([item[0]])
    L = [L_1]
    k = 2
    while (len(L[k - 2]) > 0):
        Lk_1 = L[k - 2]
        Ck = candidates_from(Lk_1, k-1)
        # print('候选{}项集是{}'.format(k, Ck))
        # print('-------------')
        x = Get_item_min_sup(Ck, L1)

        Tgt = get_Transaction_ID(x, L1)  # 获取了候选项集的要扫描数据库的索引号
        LKK = Scan(Tgt, Ck, dataset, minsup,trans)
        print(f"-----------------------FREQUENT {k}-ITEMSET--------------------------------")
        print(LKK)
        print("-------------------------------------------------------------------------")
        print()
        L.append(LKK)
        k += 1
    return L

def generateRules(FreqItems,confidence,D):
    s = []
    r = []
    length = 0
    count = 1
    inc1 = 0
    inc2 = 0
    num = 1
    m = []
    L=[]
    for i in range(1,len(FreqItems)-1):
        L.append(FreqItems[i])


    print("---------------------ASSOCIATION RULES----------------------------------")
    print("          RULES                \tSUPPORT    \t CONFIDENCE")
    print("------------------------------------------------------------------------")
    for list in L:
        for l in list:
            length = len(l)
            count = 1
            while count < length:
                s = []
                r = findsubsets(l, count)
                count += 1
                for item in r:
                    inc1 = 0
                    inc2 = 0
                    s = []
                    m = []
                    for i in item:
                        s.append(i)
                    for T in D:
                        if set(s).issubset(set(T)) == True:
                            inc1 += 1
                        if set(l).issubset(set(T)) == True:
                            inc2 += 1
                    if 100 * inc2 / inc1 >= confidence:
                        for index in l:
                            if index not in s:
                                m.append(index)
                        print("Rule#  {} : {} ==> {}     {}       {}".format(num, s, m, 100 * inc2 / len(D),
                                                                             100 * inc2 / inc1))
                        num += 1


if __name__ == "__main__":
    # read data
    minsup = 0.01
    confidence=70      #输入% 百分制
    dataset, data, trans = Read_Data('D:\综述实验2\关联规则\模块2/data12w离散化.csv')
    t1=time.time()
    L=M_Apriori(dataset, data, minsup,trans)
    t2=time.time()
    print(t2-t1)
    # generateRules(L,confidence,dataset)
