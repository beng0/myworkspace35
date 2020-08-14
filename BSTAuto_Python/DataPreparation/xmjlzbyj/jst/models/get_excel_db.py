from pandas import read_excel
from lmf.dbv2 import db_write



def read_excel_2_db(conp,filename,table_name,if_exists="replace"):
    """
    :param conp:
    :param filename: 文件路径
    :param table_name: 表明
    :param if_exists: replace 替换, append 追加
    :return:
    """

    result = read_excel(filename, sheet_name='Sheet1', converters={'person_key': str})

    for column in result.columns:
        result[column] = result[column].astype(object)
    db_write(result,table_name,dbtype="postgresql",datadict='postgresql-text',conp=conp,if_exists=if_exists)
    print("导入成功")



