## 获取要测试的企业列表放在qylist文件夹内,按照模板文件格式

## 测试企业业绩
1.run get_jst_zhiding_qyyj.py获取建设通的企业业绩excel表
2.在跳板机上 run getbst_qyyj.py获取标事通企业业绩excel表
3.run te_qyyj_bst_ishave_byexcel.py比较建设通和标事通的企业业绩

注意：可以手动查询标事通企业业绩，查询sql为：
```
SELECT href,zhongbiaoren,gg_name,diqu,xmjl,fabu_time,quyu 
FROM "gg_meta" where zhongbiaoren='云南华固建设集团有限公司' ORDER BY fabu_time desc;
```

## 测试项目经理业绩
1.需要手机企业和项目经理列表，按照模本文件放到xmjl_list文件夹内
2.run get_jst_xmjl.py获取建设通项目经理业绩
3.run getbst_xmjlyj.py获取标事通项目经理业绩
或使用以下语句手动查询项目经理业绩：
```
SELECT unnest(ry_zhongbiao_info)::jsonb->>'href',entname,name,
unnest(ry_zhongbiao_info)::jsonb->>'gg_name',xzqh,unnest(ry_zhongbiao_info)::jsonb->>'fabu_time',
person_key,unnest(ry_zhongbiao_info)::jsonb->>'quyu' 
FROM "app_ry_query" where entname = '丽江金石建筑有限责任公司' and name = '章仕成' 
ORDER BY unnest(ry_zhongbiao_info)::jsonb->>'fabu_time' desc;
```
4.run te_xmjlyeji_bst_ishave_byexcel.py对比建设通和标事通的项目经理业绩

## 测试企业资质
1.
