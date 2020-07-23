function getText(){
	var txt = document.querySelector('.win-list-w>ul>.win-list-item:nth-child(1)>.win-item-cont>.win-item-tit a').innerHtml
	len = document.querySelectorAll('.win-list-w>ul>.win-list-item').length;
	for(var i=2;i<len+1;i++){
		sel = '.win-list-w>ul>.win-list-item:nth-child('+i+')>.win-item-cont>.win-item-tit a';
		txt = txt+ '<br>'+document.querySelector(sel).innerHtml;
	}
	// document.write(txt)
	document.querySelector('.res-num').innerHtml=txt
}
getText()

 li = [
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "陈旭",
        "IDCard18": "140107199104191211",
        "SPECIALTYTYPENAME": "专职安全生产管理人员（C证）",
        "CertNum": "晋建安C（2020）0001864",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 2,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "董纪伟",
        "IDCard18": "140181199105180251",
        "SPECIALTYTYPENAME": "专职安全生产管理人员（C证）",
        "CertNum": "晋建安C（2020）0001863",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 6,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "付晓",
        "IDCard18": "140181198912214732",
        "SPECIALTYTYPENAME": "专职安全生产管理人员（C证）",
        "CertNum": "晋建安C（2020）0001865",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 10,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "常永平",
        "IDCard18": "149001197108152215",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2017）0000561",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 1,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "杜贺",
        "IDCard18": "140109198402016831",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2014）0002160",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 7,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "范国良",
        "IDCard18": "142725197202063633",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2017）0000562",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 8,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "冯玉国",
        "IDCard18": "142223198005114512",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2014）0002161",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 9,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "成晓勇",
        "IDCard18": "142322198401040091",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2020）0001345",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 3,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "褚小亮",
        "IDCard18": "130681198306105312",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2017）0000577",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 4,
        "total": 348
    },
    {
        "CorpName": "山西西山金信建筑有限公司",
        "CorpCode": "91140181814080273R",
        "PersonName": "邓浩",
        "IDCard18": "140181198508074715",
        "SPECIALTYTYPENAME": "项目负责人（B证）",
        "CertNum": "晋建安B（2020）0001346",
        "AwardDate": "2020-01-20T00:00:00",
        "EffectDate": "2023-01-20T00:00:00",
        "Row_Num": 5,
        "total": 348
    }
]
names = ''
for(var i=0;i<li.length;i++){
	names = names + li[i].PersionName
}