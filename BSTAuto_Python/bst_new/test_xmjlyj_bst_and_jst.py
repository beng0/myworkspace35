from util.my_read_excel import *
from util.my_to_excel import *
from datetime import datetime


def bsthas_isjst_xmjlyj(bst_xmjlyj_data,jst_xmjlyj_data,outfilename_bst):
    bst_data = []
    ggname_left5=" "
    # 检查标事通项目经理业绩建设通是否有
    for row in bst_xmjlyj_data:
        zhongbiaoren = row[2].strip()
        xmjl = row[3].strip()
        ggname_left5 = (row[4].strip())[:6]
        jst_ishas = "无"
        for row_jst in jst_xmjlyj_data:
            zhongbiaoren_jst = row_jst[1].strip()
            xmjl_jst = row_jst[2].strip()
            ggname_left5_jst = (row_jst[3].strip())[:6]

            if (zhongbiaoren == zhongbiaoren_jst) & (xmjl == xmjl_jst) & (ggname_left5 == ggname_left5_jst):
                jst_ishas = "有"
                break
        tmp = [row[0].strip(), str(row[1]).strip(), row[2].strip(), row[3].strip(), row[4].strip(), str(row[5]).strip(),
               row[6].strip(), str(row[7]).strip(),ggname_left5 ,"bst", jst_ishas, "有"]
        bst_data.append(tmp)
        print(bst_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href", "xzqh", "zhongbiaoren", "xmjl", "ggname", "quyu", "zbtime", "html_key", "ggname_left5","标志", "建设通是否有", "标事通是否有"]
    wirteDataToExcel(outfilename_bst + tablenamehouzui + ".xlsx", "Sheet1", columnRows, bst_data)
    print("bsthas_isjst_xmjlyj  to  excel  success")


def jsthas_isbst_xmjlyj(bst_xmjlyj_data,jst_xmjlyj_data,outfilename_jst):
    jst_data = []
    ggname_left5=' '
    # 检查jst有的项目经理业绩bst是否有
    for row in jst_xmjlyj_data:
        zhongbiaoren = row[1].strip()
        xmjl = row[2].strip()
        ggname_left5 = (row[3].strip())[:6]
        bst_ishas = "无"
        for row_bst in bst_xmjlyj_data:
            zhongbiaoren_bst = row_bst[2].strip()
            xmjl_bst = row_bst[3].strip()
            ggname_left5_bst = (row[4].strip())[:6]

            if (zhongbiaoren == zhongbiaoren_bst) & (xmjl == xmjl_bst) & (ggname_left5 == ggname_left5_bst):
                bst_ishas = "有"
                break
        tmp = [row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(),
               str(row[6]).strip(), row[7].strip(), row[8].strip(),ggname_left5,"jst", "有",bst_ishas]
        jst_data.append(tmp)
        print(jst_data)

    tablenamehouzui = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 到数据到excle中
    columnRows = ["href","zhongbiaoren", "xmjl", "ggname", "zbdq", "zbtime","zbsl_count", "zbly","zbly_href", "ggname_left5","标志", "建设通是否有", "标事通是否有"]
    wirteDataToExcel(outfilename_jst + tablenamehouzui + ".xlsx", "Sheet1", columnRows, jst_data)
    print("jsthas_isbst_xmjlyj  to  excel  success")


if __name__=='__main__':
    root_dir = os.path.dirname(os.path.abspath('.')) + '/bst_new/data'
    infilename_bst_xmjlyj = root_dir + r"\get_bst_xmjlyj\广东_云南_山西_bst_xmjlyj_获取结果_胡金花_20200727_144655.xlsx"
    outfilename_bst = root_dir + r"\test_xmjl_result\广东_云南_山西_bstxmjl业绩_jst是否有_胡金花_"
    infilename_jst_xmjlyj = root_dir + r"\get_jst_xmjlyj\广东_云南_山西_jst_xmjlyj_获取结果_胡金花_20200727_140609.xlsx"
    outfilename_jst = root_dir + r"\test_xmjl_result\广东_云南_山西_jstxmjl业绩_bsj是否有_胡金花_"

    print(infilename_bst_xmjlyj)
    # 读取标事通项目经理业绩
    all_sheet_data1 = read_excel(infilename_bst_xmjlyj)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    bst_xmjlyj_data = all_sheet_data1[0][1][1:]
    print(bst_xmjlyj_data)

    # 读取建设通项目经理业绩
    all_sheet_data2 = read_excel(infilename_jst_xmjlyj)
    # 得到第1个sheet中除了第一行(字段名字)的所有sheet数据
    jst_xmjlyj_data = all_sheet_data2[0][1][1:]
    print(jst_xmjlyj_data)

    # 检查bst有的项目经理业绩jst是否有
    bsthas_isjst_xmjlyj(bst_xmjlyj_data,jst_xmjlyj_data,outfilename_bst)

    # 检查jst有的项目经理业绩bst是否有
    jsthas_isbst_xmjlyj(bst_xmjlyj_data,jst_xmjlyj_data,outfilename_jst)

