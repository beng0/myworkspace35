

datalist=['90']

for zbsl in datalist:
    zbsl_count = int(zbsl)
    # print(zbsl)
    # 计算该企业中标有几页数据
    zbsl_count = int(zbsl)

    print(zbsl_count%15)
    if zbsl_count > 15:
        if  zbsl_count % 15  == 0 : total_ye = zbsl_count //15
        else:total_ye = zbsl_count //15 + 1

    else: total_ye = 1
    print(total_ye)