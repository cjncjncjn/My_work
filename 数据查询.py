import pandas as pd
import pymysql
import re
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="219.146.91.110",
  database="zhida_project_dev",
  user="zhidadev",
  password="zhidaefw73@T6",
  port=13306,
  charset='utf8'
 )
cursor = dbconn.cursor()
data = pd.read_excel('E:\My_code\My_work\my_6.6\data\AB股上市企业匹配产业链标签-V2_1.xlsx')
list_data = []
for i in data['公司全称']:
    # sqlcmd = "select id,name from dwd_company where  name ='{}'".format(str(i))
    # sqlcmd = "select b.scope from dwd_company a join dwd_company_eci b on a.id=b.company_id where a.name='广州白云国际机场股份有限公司'"
    sqlcmd = "select a.name,b.scope from dwd_company a join dwd_company_eci b on a.id=b.company_id where a.name='{}'".format(i)
    # sqlcmd = "select company.name,company_eci.scope from dwd_company company join dwd_company_eci company_eci on company.id=company_eci.company_id where company.name='{}'".format(i)
    print('查询中：',sqlcmd)
    exe = cursor.execute(sqlcmd)
    aa = cursor.fetchall()
    list_data.append(str(aa))
# print(list_data)
path = '.\data\本地产业链.csv'
for i in list_data:
    text = ''.join(i)
    res = re.compile("[^(^)]")
    text = ''.join(res.findall(text))
    text = ''.join(text.strip().split("'"))
    name1 = text.split(',',maxsplit=1)[0]
    try:
        text = text.split(',',maxsplit=1)[1]
    except :
        continue
    print(text.split('；'))
    if len(text.split('；')) == 1:
        text_list = text.split(',')
    else:
        text_list = text.split('；')
    name_text = ';'.join(text_list[:3])
    name_text = name_text[:80]
    with open(path, 'a', encoding='utf-8') as f:
        f.write("{},{}\n".format(name1,name_text))
dbconn.close()