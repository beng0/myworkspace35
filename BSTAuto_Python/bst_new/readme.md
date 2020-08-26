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