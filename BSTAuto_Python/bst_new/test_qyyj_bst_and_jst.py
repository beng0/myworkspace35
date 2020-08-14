from util.my_read_excel import *
from util.my_to_excel import *
from datetime import datetime


def bsthas_isjst_qyyj(bst_qyyj_data,jst_qyyj_data,outfilename_bst):
    bst_data = []
    ggname_left5 = " "
    # 检查标事通企业业绩建设通是否有
    for row in bst_qyyj_data:
        zhongbiaoren = row[4]
        ggname_left5 = (row[2])[:6]
        jst_ishas = "无"
        for row_jst in jst_qyyj_data:
            zhongbiaoren_jst = row_jst[2]
            ggname_left5_jst = (row_jst[3])[:6]

            if (zhongbiaoren == zhongbiaoren_jst) & (ggname_left5 == ggname_left5_jst):
                jst_ishas = "有"
                break
        tmp = [row[0], row[1], row[2], str(row[3]), row[4], str(row[5]),row[6],ggname_left5,"bst",jst_ishas, "有"]
        bst_data.append(tmp)
        print(bst_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "diyu", "gg_name", "ent_key", "entname", "html_key", "fabu_time", "ggname_left5", "标志","建设通是否有", "标事通是否有"]
    wirteDataToExcel(outfilename_bst + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, bst_data)


def jsthas_isbst_qyyj(bst_qyyj_data,jst_qyyj_data,outfilename_jst):
    jst_data = []
    ggname_left5 =  " "
    # 检查jst有的企业业绩bst是否有
    for row in jst_qyyj_data:
        zhongbiaoren = row[2]
        ggname_left5 = (row[3])[:6]
        bst_ishas = "无"
        for row_bst in bst_qyyj_data:
            zhongbiaoren_bst = row_bst[4]
            ggname_left5_bst = (row_bst[2])[:6]

            if (zhongbiaoren == zhongbiaoren_bst)  & (ggname_left5 == ggname_left5_bst):
                bst_ishas = "有"
                break
        tmp = [row[0], row[1], row[2], row[3], row[4], row[5],row[6], row[7], ggname_left5,"jst","有",bst_ishas]

        jst_data.append(tmp)
        print(jst_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "shi","zhongbiaoren", "ggname", "diqu" , "xmjl", "zbtime", "zbly","ggname_left5","标志", "建设通是否有", "标事通是否有"]
    wirteDataToExcel(outfilename_jst + tablenamehouzui + ".xlsx", "jst_qyyj_zhejiang", columnRows, jst_data)


if __name__=='__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/bst_new/data'
    infilename_bst_qyyj = root_dir + r"\get_bst_qyyj\广东_云南_山西_bst_qyyj_get结果_胡金花_20200727_144002.xlsx"
    outfilename_bst = root_dir + r"\test_qyyj_result\广东_云南_山西_bst企业业绩_jst是否有_胡金花_"
    infilename_jst_qyyj = root_dir + r"\get_jst_qyyj\广东_云南_山西建设通企业业绩_胡金花_20200727_115212.xlsx"
    outfilename_jst = root_dir + r"\test_qyyj_result\广东_云南_山西_jst企业业绩_bsj是否有_胡金花_"

    # 读取标事通企业业绩
    all_sheet_data1 = read_excel(infilename_bst_qyyj)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    bst_qyyj_data = all_sheet_data1[0][1][1:]
    print(bst_qyyj_data)

    # 读取建设通企业业绩
    all_sheet_data2 = read_excel(infilename_jst_qyyj)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    jst_qyyj_data = all_sheet_data2[0][1][1:]
    print(jst_qyyj_data)

    # 检查bst有的企业业绩jst是否有
    bsthas_isjst_qyyj(bst_qyyj_data,jst_qyyj_data,outfilename_bst)

    # # 检查jst有的企业业绩bst是否有
    jsthas_isbst_qyyj(bst_qyyj_data,jst_qyyj_data,outfilename_jst)

