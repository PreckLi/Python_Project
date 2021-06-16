import csv
import re
import json


def PPTdeal(ppt_file_name, sum_cost):
    list = []
    with open(ppt_file_name, "r", encoding='utf-8-sig') as proportion_file:
        ppt_reader = csv.reader(proportion_file)
        for i in ppt_reader:
            list.append(i)
        sum = 0
        for i in list:
            sum += float(i[1])
        proportion = []
        es_list = []
        for i in list:
            proportion.append(float(i[1]) / sum)
            es_list.append(i[0].strip('\t'))
        count = 0
        dict = {}
        for i in es_list:
            dict[i] = sum_cost * proportion[count]
            if i not in wholedict:  # 如果键值对不存在就初始化为0
                wholedict[i] = 0
            wholedict[i] += dict[i]
            count += 1


merge_file_name = "merge_202105.csv"
wholedict = {}  # 实例总字典
ecs_xm_cost = 0
es_xm_cost = 0
rds_xm_cost = 0
yunpan_xm_cost = 0
xm_cost = 0
cp_cost = 0
this_month_cost = 1207447.28
ideal_xm_cost = this_month_cost * 0.4
has_special_es = False
ecs_list = []
rd_list = []  # 数量在1~5区间内分入研发中台的id列表

with open(merge_file_name, 'r', encoding='utf-8-sig') as mergefile0:
    merge0_reader = csv.reader(mergefile0)
    for row in merge0_reader:
        if row[4] == "云服务器 ECS":
            ecs_list.append(row)

with open(merge_file_name, 'r', encoding='utf-8-sig', newline='') as mergefile:
    merge_reader = csv.reader(mergefile)
    research_devlopment_price = 0
    rds_research_devlopment_price = 0
    ecs_research_devlopment_price = 0
    es_research_devlopment_price = 0
    yunpan_ecs = ""
    rds_rd_list = []
    for row in merge_reader:
        """确定类型"""
        if row[32] == "" and row[5] != "关系型数据库RDS(包月)" and row[5] != "云盘":
            continue
        if row[4] == "Elasticsearch":
            type = "es"
        elif row[4] == "云服务器 ECS":
            type = "ecs"
        elif row[5] == "关系型数据库RDS(包月)":
            type = "rds"
        elif row[5] == "云盘":
            type = "yunpan"

        """确定分摊数量"""
        if type == "ecs":
            if len(row[32].split(";")[1].split("-")) == 4:  # 未打标签的，暂时跳过
                continue
            share = row[32].split(";")[1].split("-")[4]  # share为最后一个字符段
            # print("share:", share)
            if share[0:3] == "AVG":
                share_num = int(share.split("_")[1])  # share_num为分摊个数
            if share[0:3] == "IDP":
                share_num = 1
        if type == "es":
            share = row[32].split("_")[1].split("-")[4]
            if share == "IDP":
                share_num = 1
            if share == "AVG":
                share_num = int(row[32].split("_")[2])

        if type == "rds":
            if row[33] == "":
                rds_research_devlopment_price += float(row[24])
                rds_rd_list.append(row[9])
                continue
            share = row[32].split("-")[2]
            if share == "IDP":
                share_num = 1
            else:
                share_num = int(share.split("_")[1])
        if type == "yunpan":
            flag1 = 1
            ecsid = row[13].split(":")[-1]
            if ecsid == "-":
                flag1 = 0
            for ecsrow in ecs_list:
                if ecsrow[9] == ecsid:
                    if ecsrow[32] == "" or row[13] == "-":  # 若第32列为空，则此云盘挂载的ecs为产品或无关联ecs，此云盘不计入项目
                        flag1 = 0
                        break
                    if len(ecsrow[32].split(";")[1].split("-")) == 4:  # 未打标签的，暂时跳过
                        flag1 = 0
                        break
                    share = ecsrow[32].split(";")[1].split("-")[4]
                    yunpan_ecs = ecsrow
                    if share[0:3] == "IDP":
                        share_num = 1
                    if share[0:3] == "AVG":
                        share_num = int(share.split("_")[1])
            if flag1 == 0:
                continue

        """列出分摊列表"""
        if type == "ecs":
            share_list = re.split(r'[;,\s]', row[33].strip("[").strip("]").strip("{").strip("}").strip("TagKey=").strip(
                "TagValue=").replace("TagValue=}, {TagKey=", ""))  # share_list截取出分摊对象的列表
        elif type == "es":
            share_json = json.loads(row[33])
            # print("ecs_json:", share_json)
            share_list = []
            cost_list = []
            for json_i in share_json:
                # print(json_i["tagKey"])
                share_list.append(json_i["tagKey"])
                if json_i["tagValue"] != "":
                    cost_list.append(json_i["tagValue"])
                # if json_i["tagKey"].split(";"):
            del (share_list[0])  # 第一项为默认标签，需要删除
            del (cost_list[0])
        elif type == "rds":
            share_list = re.split(r'[;|\s]', row[33])
            count1 = 0
            for i in share_list:
                if i[-1] == ":":
                    share_list[count1] = i[:-1]
                count1 += 1
        elif type == "yunpan":
            share_list = re.split(r'[;,\s]',
                                  yunpan_ecs[33].strip("[").strip("]").strip("{").strip("}").strip("TagKey=").strip(
                                      "TagValue=").replace("TagValue=}, {TagKey=", ""))  # share_list截取出分摊对象的列表

        elif type != "es" and type != "ecs" and type != "rds" and type != "yunpan":  # 排除ecs,es,rds,yunpan的项先默认为空
            share_list = []
        share_dict = {}
        # 清除列表内空值
        while '' in share_list:
            share_list.remove('')

        """产品，项目类"""
        if type == "ecs":
            flag = row[32].split(";")[1].split("-")[2]
        elif type == "es":
            flag = row[32].split("_")[1].split("-")[2]
        elif type == "rds":
            flag = row[32].split("-")[1]
        elif type == "yunpan":
            flag = yunpan_ecs[32].split(";")[1].split("-")[2]
        elif type != "es" and type != "ecs" and type != "rds" and type != "yunpan":
            flag = "WZ"

        if (flag == "XM" or flag == "CP"):  # 若为项目或产品
            # print(share)
            for i in share_list:
                key = i  # 生成一个实例对应的项目或产品字典
                share_dict[key] = 0
                if key not in wholedict:  # 如果键值对不存在就初始化为0
                    wholedict[key] = 0
            wholeprice = float(row[24])
            # print("wholeprice", wholeprice)
            if share_num == 1:  # 独占资源全部分摊
                avg_price = wholeprice
                for key in share_dict:
                    share_dict[key] = avg_price
                    wholedict[key] += avg_price
            if 1 < share_num < 5:  # 分摊数5个以内
                avg_price = wholeprice / 5
                for key in share_dict:
                    share_dict[key] = avg_price
                    wholedict[key] += avg_price
                    # print("分摊费用:", share_dict[key])
                research_devlopment_price += wholeprice - avg_price * share_num  # 剩余由研发中台分摊
                rd_list.append(row[9])
                if type == "ecs":
                    ecs_research_devlopment_price += wholeprice - avg_price * share_num
                elif type == "es":
                    es_research_devlopment_price += wholeprice - avg_price * share_num
            if 5 <= share_num <= 20:  # 分摊数5到20之间
                avg_price = wholeprice / 5
                # print("avg_price", avg_price)
                for i, (key, value) in enumerate(share_dict.items()):  # 前五人分摊
                    if i in range(5):
                        share_dict[key] = avg_price
                        wholedict[key] += avg_price
                        # print(key, share_dict[key])
            if share_num > 20:  # 分摊数超过20
                avg_price = wholeprice / 20
                for i, (key, value) in enumerate(share_dict.items()):  # 前二十人分摊
                    if i in range(20):
                        share_dict[key] = avg_price
                        wholedict[key] += avg_price
                        # print(key, share_dict[key])
            print(row[9], row[6], ":")
            for key in share_dict:
                print(key, ":", share_dict[key], key[0:2])
                if type == "ecs":
                    if key[0:2] == "项目":
                        ecs_xm_cost += share_dict[key]
                if type == "es":
                    if key[0:2] == "项目":
                        es_xm_cost += share_dict[key]
                if type == "rds":
                    if key[0:2] == "项目":
                        rds_xm_cost += share_dict[key]
                if type == "yunpan":
                    if key[0:2] == "项目":
                        yunpan_xm_cost += share_dict[key]
            print("--------------------")

        """综合类有产品和项目"""
        if flag == "ZH":  # 产品项目混用
            for i in share_list:
                key = i  # 生成一个实例对应的项目或产品字典
                share_dict[key] = 0
                if key not in wholedict:  # 如果键值对不存在就初始化为0
                    wholedict[key] = 0
            wholeprice = float(row[24])
            # 按比例分配
            if share == "PPT":
                sum = 0
                for i in cost_list:
                    sum += int(i)
                proportion = []  # 分摊列表
                for i in cost_list:
                    proportion.append(int(i) / sum)
                count = 0
                for i in share_list:
                    share_dict[i] = wholeprice * proportion[count]
                    wholedict[i] += share_dict[i]
                    count += 1

            # 产品，项目均分
            if share != "PPT":
                cp_price = wholeprice / 2
                xm_price = wholeprice / 2
                cp_num = 0
                xm_num = 0
                for key in share_dict:  # 统计综合实例中产品和项目数量
                    if key.split("-")[0] == "产品":
                        cp_num += 1
                    if key.split("-")[0] == "项目":
                        xm_num += 1
                # 产品，项目分别再按不同数量规则分摊
                if 1 < cp_num < 5:
                    avg_cp_price = cp_price / 5
                    for key in share_dict:
                        if key.split(",")[0].split("-")[0] == "产品":
                            share_dict[key] = avg_cp_price
                            wholedict[key] += avg_cp_price
                    research_devlopment_price += cp_price - avg_cp_price * cp_num  # 剩余由研发中台分摊
                    rd_list.append(row[9])
                    if type == "ecs":
                        ecs_research_devlopment_price += cp_price - avg_cp_price * cp_num
                    elif type == "es":
                        es_research_devlopment_price += cp_price - avg_cp_price * cp_num
                if 1 < xm_num < 5:
                    avg_xm_price = xm_price / 5
                    for key in share_dict:
                        if key.split(",")[0].split("-")[0] == "项目":
                            share_dict[key] = avg_xm_price
                            wholedict[key] += avg_xm_price
                    research_devlopment_price += xm_price - avg_xm_price * xm_num  # 剩余由研发中台分摊
                    if type == "ecs":
                        ecs_research_devlopment_price += xm_price - avg_xm_price * xm_num
                    elif type == "es":
                        es_research_devlopment_price += xm_price - avg_xm_price * xm_num
                if 5 <= cp_num <= 20:  # 分摊数5到20之间
                    avg_cp_price = cp_price / 5
                    # print("avg_price", avg_price)
                    for i, (key, value) in enumerate(share_dict.items()):  # 产品前五人分摊
                        if i in range(5):
                            if key.split(",")[0].split("-")[0] == "产品":
                                share_dict[key] = avg_cp_price
                                wholedict[key] += avg_cp_price
                if 5 <= xm_num <= 20:  # 分摊数5到20之间
                    avg_xm_price = xm_price / 5
                    # print("avg_price", avg_price)
                    for i, (key, value) in enumerate(share_dict.items()):  # 项目前五人分摊
                        if i in range(5):
                            if key.split(",")[0].split("-")[0] == "项目":
                                share_dict[key] = avg_xm_price
                                wholedict[key] += avg_xm_price

                if cp_num > 20:
                    avg_cp_price = cp_price / 20
                    for i, (key, value) in enumerate(share_dict.items()):  # 前二十人分摊
                        if i in range(20):
                            if key.split(",")[0].split("-")[0] == "产品":
                                share_dict[key] = avg_cp_price
                                wholedict[key] += avg_cp_price
                if xm_num > 20:
                    avg_xm_price = xm_price / 20
                    for i, (key, value) in enumerate(share_dict.items()):  # 前二十人分摊
                        if i in range(20):
                            if key.split(",")[0].split("-")[0] == "项目":
                                share_dict[key] = avg_xm_price
                                wholedict[key] += avg_xm_price

            print(row[9], row[6], ":")
            for key in share_dict:
                print(key, ":", share_dict[key], "元", key[0:2])
                if type == "ecs":
                    if key[0:2] == "项目":
                        ecs_xm_cost += share_dict[key]
                if type == "es":
                    if key[0:2] == "项目":
                        es_xm_cost += share_dict[key]
                if type == "rds":
                    if key[0:2] == "项目":
                        rds_xm_cost += share_dict[key]
                if type == "yunpan":
                    if key[0:2] == "项目":
                        yunpan_xm_cost += share_dict[key]
            print("--------------------")

print("总分摊费用如下：")
for key in wholedict:
    if key[0:2] == "产品":
        cp_cost += wholedict[key]
    if key[0:2] == "项目":
        xm_cost += wholedict[key]

for key in wholedict:
    print(key, ":", round(wholedict[key], 2))
print("#################################################")
print("产品费用：", round(this_month_cost - xm_cost, 2))
print("项目费用：", round(xm_cost, 2))
print("ecs分入研发中台费用(包含云盘):", round(research_devlopment_price, 2))
research_devlopment_price += rds_research_devlopment_price
print("es分入研发中台费用:", round(es_research_devlopment_price, 2))
print("rds分入研发中台费用：", round(rds_research_devlopment_price, 2))
print("研发中台分摊：", round(research_devlopment_price, 2))
print("未算研发中台的产品费用:", round(this_month_cost - xm_cost - research_devlopment_price, 2))
print("ecs的项目费用:", round(ecs_xm_cost, 2))
print("es的项目费用:", round(es_xm_cost, 2))
print("rds的项目费用:", round(rds_xm_cost, 2))
print("云盘的项目费用：", round(yunpan_xm_cost, 2))
print("#################################################")
print("未明确放入研发中台的实例id（目前包含rds未明确的实例）：")
print(list(set(rds_rd_list)))
print("数量1~5之间放入研发中台的实例id：")
print(rd_list)
