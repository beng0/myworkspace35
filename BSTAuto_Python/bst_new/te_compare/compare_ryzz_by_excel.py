from BSTAuto_Python.bst_new.compareBase.CompareClass import *

root_dir = os.path.dirname(os.path.abspath('.')) + '\\data'
infilename1 = root_dir + r"\get_sheng_ryzz_qyzz\云南_省平台xmjlzzwithzzcode_贺家斌_20201216_142601.xlsx"
infilename2 = root_dir + r"\get_bst_ryzz_qyzz\云南bst人员资质_贺家斌_20201215_145515.xlsx"
outfilename = root_dir + r"\hebin\云南人员资质对比结果_贺家斌_"

columnRows = ["entname", "name", "zjhm", "zsbh", "zclb", "zhuanye", "ryzz_code", "省平台是否有", "标事通是否有"]
hebin_columnRows = ["entname", "name", "zjhm", "zsbh", "zclb", "zhuanye", "ryzz_code"]
comp = CompareClass(infilenames=[infilename1, infilename2], num=[0, 1, 6],
                    outfilename=outfilename, columnRows=columnRows)
hebin_filename = root_dir + r"\hebin\云南省平台_标事通_人员资质合并_贺家斌_"
hebin_filename = comp.get_hebin_data(hebin_filename=hebin_filename,columnRows=hebin_columnRows)
comp.get_compare_result(hebin_filename=hebin_filename)
