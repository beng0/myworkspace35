from BSTAuto_Python.bst_new.compareBase.CompareClass import *

root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
infilename1 = root_dir + r"\jianyu\剑鱼标讯_20201217_104412.xlsx"
infilename2 = root_dir + r"\get_bst_gg\标事通标讯_数据准备_贺家斌_20201217_104918.xlsx"
outfilename = root_dir + r"\hebin\云南标讯_标事通_剑鱼_对比结果_贺家斌_"

columnRows = ["keyword", "gg_name", "fabu_time", "html_key", "左10", "剑鱼是否有", "标事通是否有"]
hebin_columnRows = ["keyword", "gg_name", "fabu_time", "html_key"]
hebin_filename = root_dir + r"\hebin\云南剑鱼_标事通_标讯合并_贺家斌_"
comp = CompareClass(infilenames=[infilename1, infilename2], num=[4],
                    outfilename=outfilename, columnRows=columnRows)
hebin_filename = comp.get_hebin_data(hebin_filename=hebin_filename,columnRows=hebin_columnRows)
comp.get_compare_result(hebin_filename=hebin_filename)
