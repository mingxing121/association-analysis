from method import association_rules
import csv



path = 'D:\综述实验2\关联规则\模块2/data12w离散化.csv'
data = []
with open(path, 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        row = list(set(row))  # 去重，排序
        row.sort()
        data.append(row)  # 将添加好的数据添加到数组



min_support = 0.01 # 最小支持度
min_conf = 0.7  # 最小置信度

fp = association_rules.Fp_growth()
rule_list = fp.generate_R(data, min_support, min_conf, len(data))
association_rules.find_rule(rule_list)
print(len(rule_list))
