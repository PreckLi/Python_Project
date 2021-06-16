import csv


'''以账单表为基础，将账单表和ecs,es,rds合并，生成合并表'''
instance_file_name = 'ecs610.csv'
es_file_name = 'es607.csv'
yunpan_file_name = 'yunpan607.csv'
cost_file_name = '202105_cost.csv'
rds_file_name = 'rds607.csv'
merge_file_name = 'merge_202105.csv'
# merge_file_name_final = 'mergedemofinal527.csv'

cost_rowlist = []  # 账单列表
instance_rowlist = []  # ecs列表
es_rowlist = []  # es列表
yunpan_list = []  # 云盘列表
rds_list = []  # rds列表
# 添加列表
with open(cost_file_name, 'r', encoding='utf-8-sig') as cost_file, \
        open(instance_file_name, 'r', encoding='utf-8-sig') as instance_file, \
        open(es_file_name, 'r', encoding='utf-8-sig') as es_file, \
        open(yunpan_file_name, 'r', encoding='utf-8-sig') as yunpan_file, \
        open(rds_file_name, 'r', encoding='utf-8-sig') as rds_file:
    cost_reader = csv.reader(cost_file)
    instance_reader = csv.reader(instance_file)
    es_reader = csv.reader(es_file)
    yunpan_reader = csv.reader(yunpan_file)
    rds_reader = csv.reader(rds_file)
    for cost_row in cost_reader:
        # print('花费:',cost_row)
        cost_rowlist.append(cost_row)
    for instance_row in instance_reader:
        # print('实例:',instance_row)
        instance_rowlist.append(instance_row)
    for es_row in es_reader:
        # print('es:',instance_row)
        es_rowlist.append(es_row)
    for yunpan_row in yunpan_reader:
        # print('云盘:',yunpan_row)
        yunpan_list.append(yunpan_row)
    for rds_row in rds_reader:
        rds_list.append(rds_row)

count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0

with open(merge_file_name, 'a+', encoding='utf-8-sig', newline='') as mergefile:
    merge_writer = csv.writer(mergefile)
    for row1 in cost_rowlist:
        flag = 1  # flag是标记位，匹配成功后就不插入20个空值了，若匹配失败则插入20个空值
        for row2 in instance_rowlist:
            if row1[9] == row2[0]:  # ecs匹配成功
                flag = 0
                temprow = row2[2:]  # instance.csv的前两列重复，去掉
                row1.extend(temprow)  # 列表合并
                # row1=list(set(row1))#列表去重
                # row1.sort()#列表排序
                count1 += 1
                # print(row1)
                merge_writer.writerow(row1)
        for row3 in es_rowlist:
            if row1[9] == row3[0]:  # es匹配成功
                flag = 0
                temprow = row3[2:]
                row1.extend(temprow)
                count3 += 1
                merge_writer.writerow(row1)
        for row4 in rds_list:
            if row1[9] == row4[0]:  # rds匹配成功
                flag = 0
                temprow = row4[1:]
                row1.extend(temprow)
                count4 += 1
                merge_writer.writerow(row1)

        if flag != 0:  # 匹配失败
            row1.extend(
                ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])  # 匹配不到的id添加20个空字符
            merge_writer.writerow(row1)
        count2 += 1

"""以下为合成带云盘费用的merge表，直接可通过计算ecs费用以同时完成挂载云盘的费用，此法无法明确每个云盘下各项目产品分别分摊多少钱，现被注释"""
# merge_list = []
# with open(yunpan_file_name, 'r', encoding='utf-8-sig') as yunpan_file, open(merge_file_name, 'r',
#                                                                             encoding='utf-8-sig') as mergefile:
#     yunpan_reader = csv.reader(yunpan_file)
#     merge_reader = csv.reader(mergefile)
#     for i in merge_reader:
#         merge_list.append(i)
#     for yunpan_i in yunpan_reader:
#         if yunpan_i[1] == "-":
#             continue
#         print(yunpan_i)
#         ecsid = yunpan_i[1].split(":")[-1]
#         print("云盘挂载ecs_id:", type(ecsid), ecsid)
#         for merge_i in merge_list:
#             if ecsid == merge_i[9]:
#                 print("merge_i[9]:", type(merge_i[9]), merge_i[9])
#                 print("merge_ithen:", merge_i)
#                 merge_i[24] = float(merge_i[24])
#                 merge_i[24] += float(yunpan_i[7])
#                 print("merge_inow:", merge_i)
#
# with open(merge_file_name_final, 'a+', encoding='utf-8-sig', newline='') as merge_final_file:
#     final_writer = csv.writer(merge_final_file)
#     for i in merge_list:
#         final_writer.writerow(i)

print('ecs相等数:', count1)
print('es相等数:', count3)
print('rds相等数：', count4)
print('总数:', count2)
