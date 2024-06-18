import csv
import time
import os
import psutil

import numpy as np, itertools
import pandas as pd



FreqItems = dict()
support = dict()


def eclat(prefix, items, dict_id, cnt):
    while items:
        i, itids = items.pop()
        isupp = len(itids)
        if isupp >= minsup * cnt:

            FreqItems[frozenset(prefix + [i])] = isupp
            suffix = []
            for j, ojtids in items:
                jtids = itids & ojtids
                if len(jtids) >= minsup * cnt:
                    suffix.append((j, jtids))

            dict_id += 1
            eclat(prefix + [i], sorted(suffix, key=lambda item: len(item[1]), reverse=True), dict_id, cnt)


def rules(FreqItems, confidence):
    Rules = []
    cnt = 0

    for items, support in FreqItems.items():
        if (len(items) > 1):
            lis = []
            num = 0
            for i in range(len(items)):
                num += 1
                antecedent = list(itertools.combinations(items, num))
                lis.append(antecedent)
                if num == len(items) - 1:
                    break
            for elm in lis:
                for item in elm:
                    antecedent = item
                    consequent = set(items).difference(antecedent)

                    conf = float(FreqItems[frozenset(items)] / FreqItems[frozenset(antecedent)] * 100)
                    if (conf >= confidence):
                        # cnt += 1
                        # lift = float(conf / FreqItems[frozenset(consequent)])
                        # if lift >= 1:
                        Rules.append((antecedent, consequent, support, conf))

    print('Found %d Rules ' % (cnt))
    return Rules


def print_Frequent_Itemsets(output_FreqItems, FreqItems):
    file = open(output_FreqItems, 'w+')
    for item, support in FreqItems.items():
        file.write(" {} : {} \n".format(list(item), round(support, 4)))


def print_Rules(Rules, cnt):
    num=0
    print('--------------------------------------------------------')
    for a, b, supp, conf in sorted(Rules):
        num+=1
        print("rule #{}: {} ==> {} support: {} confidence: {} \n".format((num),(a), (b), round(supp / cnt, 4), round(conf, 4)
                                                               ))
        with open('D:\综述实验2\关联规则/book.txt', 'a+', encoding='utf-8') as file:
            file.write("rule #{}: {} ==> {} support: {} confidence: {} \n".format((num),(a), (b), round(supp / cnt, 4), round(conf, 4)
                                                               ) + '\n')
    # file.close()


def Read_Data(filename, delimiter=','):
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
    return data, trans


if __name__ == "__main__":
    minsup = 0.01
    confidence = 70
    output_FreqItems = 'output_freqitems.csv'
    dict_id = 0
    data, cnt = Read_Data('D:\综述实验2\关联规则/A类高信噪比光谱14个线指数离散化.csv')  # change the delimiter based on your input file
    data.pop("\n", None)
    data.pop("", None)
    print('finished reading data..... \n Starting mining .....')
    t1=time.time()

    eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=True), dict_id, cnt)

    t2=time.time()
    print(t2-t1)
    print('found %d Frequent items' % len(FreqItems))
    Rules = rules(FreqItems, confidence)
    print('Writing Rules .....')

    print_Frequent_Itemsets(output_FreqItems, FreqItems)
    print_Rules(Rules, cnt)
    # res = pd.DataFrame(Rules)
    # print(res)

    # res.to_csv('D:\综述实验2\关联规则/A类高信噪比关联规则.csv', index=False)

