from bst_new.util.my_read_excel import  *
from bst_new.util.my_to_excel import  *
from datetime import datetime

def readexcel_qyyj_zhiding_count(infilename,outfilename,qyyj_count):
    all_sheet_data = read_excel(infilename)
    qy_list = all_sheet_data[0][1][1:]

    count = 0
    out_qyyj_data=[]
    qyname_temp =" "
    for  qyname in  qy_list:

        if count in [0,1]: qyname_temp = qyname[4]
        if  (count > qyyj_count) & (qyname_temp == qyname[4]) :continue
        else:
            if  qyname_temp == qyname[4]:
                out_qyyj_data.append(qyname)
                count += 1
            else:
                out_qyyj_data.append(qyname)
                count = 1
        print(out_qyyj_data)

    # 到数据到excle   href	diyu	gg_name	ent_key	entname	html_key	fabu_time	ggname_left5	标志	建设通是否有	标事通是否有
    headers = ["href", "diyu", "gg_name", "ent_key", "entname", "html_key", "fabu_time", "ggname_left5", "建设通是否有", "标事通是否有","ly"]
    wirteDataToExcel2(outfilename, headers, out_qyyj_data, 0)
    print("完成")

def readexcel_qyyj_zhiding_count2(infilename,outfilename,qyyj_count):
    all_sheet_data = read_excel(infilename)
    qy_list = all_sheet_data[0][1][1:]
    print(qy_list)

    count = 0
    out_qyyj_data=[]
    qyname_temp =" "
    for  row in  qy_list:
        print(row)

        if count in [0,1]: qyname_temp = row[0]
        if  (count > qyyj_count) & (qyname_temp == row[0]) :continue
        else:
            if  qyname_temp == row[0]:
                out_qyyj_data.append(row)
                count += 1
            else:
                out_qyyj_data.append(row)
                count = 1
        print(out_qyyj_data)

    # 到数据到excle
    headers = ["qyname","xmjl"]
    wirteDataToExcel2(outfilename, headers, out_qyyj_data, 0)
    print("完成")


def readexcel_xmjlyj_zhiding_count(infilename,outfilename,qyyj_count):
    all_sheet_data = read_excel(infilename)
    xmjlyj_list = all_sheet_data[0][1][1:]

    count = 0
    out_qyyj_data=[]
    qyname_temp =" "
    xmjl_temp =" "
    for  content in  xmjlyj_list:

        if count in [0,1]:
            qyname_temp = content[2]
            xmjl_temp = content[3]

        if  (count > qyyj_count) & (qyname_temp == content[2]) & (xmjl_temp == content[3]) :continue
        else:
            if (qyname_temp == content[2]) & (xmjl_temp == content[3]):
                out_qyyj_data.append(content)
                count += 1
            else:
                out_qyyj_data.append(content)
                count = 1
        print(out_qyyj_data)

    # 到数据到excle   href	xzqh	zhongbiaoren	xmjl	ggname	quyu	zbtime	html_key	ggname_left5	标志	建设通是否有	标事通是否有
    headers = ["href","xzqh","zhongbiaoren","xmjl","ggname","quyu","zbtime","html_key","ggname_left5","建设通是否有","标事通是否有"]
    wirteDataToExcel2(outfilename, headers, out_qyyj_data, 0)
    print("完成")

if __name__=='__main__':
    tablenamehouzui = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    qyyj_count = 4
    # infilename = r"D:\SVN\数据对比\数据准备\企业中标业绩\广东\广东建设通企业业绩_数据准备_抽取企业_标事通查询结果_胡金花2020-06-04_111318.xlsx"
    # outfilename = r"D:\SVN\数据对比\数据准备\企业中标业绩\广东\广东建设通企业业绩_数据准备_抽取的企业_标事通查询结果_每个企业"+str(qyyj_count+1)+"条_胡金花_"

    # infilename = r"D:\SVN\数据对比\数据准备\企业中标业绩\云南\云南建设通企业业绩_数据准备_抽取的企业_标事通查询结果_胡金花2020-06-04_145747.xlsx"
    # outfilename = r"D:\SVN\数据对比\数据准备\企业中标业绩\云南\云南建设通企业业绩_数据准备_抽取的企业_标事通查询结果_每个企业" + str(qyyj_count + 1) + "条_胡金花_"

    # infilename = r"D:\SVN\数据对比\数据准备\企业中标业绩\山西\山西建设通企业业绩_数据准备_抽取的企业_标事通查询结果_胡金花2020-06-04_172105.xlsx"
    # outfilename = r"D:\SVN\数据对比\数据准备\企业中标业绩\山西\山西建设通企业业绩_数据准备_抽取的企业_标事通查询结果_每个企业" + str(qyyj_count + 1) + "条_胡金花_"

    root_dir = os.path.dirname(os.path.abspath('.'))
    infilename = root_dir + r"\data\test_xmjl_result\广东、云南、山西企业对比结果_20200728胡金花.xlsx"
    outfilename =root_dir+ r"\data\test_xmjl_result\广东、云南、山西企业对比结果xmjlyj_抽取的企业_每个企业" + str(qyyj_count + 1) + "条_胡金花_"
    # readexcel_qyyj_zhiding_count(infilename,outfilename+ tablenamehouzui+ ".xlsx",qyyj_count)

    readexcel_xmjlyj_zhiding_count(infilename, outfilename + tablenamehouzui + ".xlsx", qyyj_count)