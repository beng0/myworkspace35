

function getPerson(){
	var topwin = window.top.document.getElementById("nyroModalIframe").contentWindow; 
	name = topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a:nth-child(2) div>span.spec-item-name").
	innerText;
	ryzz = "<br/>"+topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a:nth-child(2) div>h5:nth-child(4)").
	innerText.trim();
	zsbh = "<br/>"+topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a:nth-child(2) div>span:nth-child(2)").
	innerText.trim().replace(/(证书编号：)/g,"");
	len = topwin.document.querySelectorAll(".wrapper-main>.container>.column-wrap>div>a").length
	for(var i=3;i<=len+1;i++){
		name1 = topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a:nth-child("+i+") div>span.spec-item-name").
	innerText;
		name = name + '<br/>' + name1;
		ryzz1 = topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a:nth-child("+i+") div>h5:nth-child(4)").
	innerText;
		ryzz = ryzz + "<br/>" + ryzz1;
		zsbh1 = topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a:nth-child("+i+") div>span:nth-child(2)").
	innerText.trim().replace(/(证书编号：)/g,"");
		zsbh = zsbh + "<br/>" + zsbh1;
	}
	document.write(name)
	document.write(ryzz)
	document.write(zsbh)
}
getPerson()


function getqyzz(){
	var qyzz_s = ''
	len_li = document.querySelectorAll("div#ent-qua>.data-list>tbody>tr").length
	for(var i=2;i<=len_li;i++){
		qyzz1 = document.querySelector("div#ent-qua>.data-list>tbody>tr:nth-child("+i+")>td:nth-child(3)").innerText
		qyzz_s = qyzz_s + qyzz1
		
	}
	qyzz_s = qyzz_s.replace(/(；)/g,"<br/>")
	document.write(qyzz_s)
	return qyzz_s
}
getqyzz()



var qyzz_s = ''
qyzz = document.querySelector("div#ent-qua>.data-list>tbody>tr:nth-child(3)>td:nth-child(3)").innerText
qyzz_s = qyzz_s + qyzz
qyzz_s = qyzz_s.replace(/(；)/g,"<br/>")
console.log(qyzz_s)


var topwin = window.top.document.
getElementById("nyroModalIframe").contentWindow;
zsbh_s = topwin.document.querySelector
	(".wrapper-main>.container>.column-wrap>div>a.doubt:nth-child(2) div>span:nth-child(2)").
	innerText.trim();
console.log(zsbh_s)
var zsbh = zsbh_s.replace(/(证书编号：)/g,"")
console.log(zsbh)
	// var patt = /证书编号：(.*)/g;
	// zsbh = patt.exec(zsbh_s)[1];
	// console.log(zsbh);