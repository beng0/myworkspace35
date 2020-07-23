function getName(){
	name = document.querySelector('.newcomp-winning-table>ul>li:nth-child(2) h2>a').innerText
	len = document.querySelectorAll('.newcomp-winning-table>ul>li').length
	for(var i=3;i<len+1;i++){
		sel = '.newcomp-winning-table>ul>li:nth-child('+i+') h2>a'
		name = name + '\n' + document.querySelector(sel).innerText
	}
	document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(1)').innerText = name
}

function getZhuanye(){
	zhuanye = document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(3)>h2').innerText
	len = document.querySelectorAll('.newcomp-winning-table>ul>li').length
	for(var i=3;i<len+1;i++){
		sel = '.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(3)>h2'
		zhuanye = zhuanye + '\n' + document.querySelector(sel).innerText
	}
	document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(4)').innerText = zhuanye
}
getName()
getZhuanye()
function getYeji(){
	yeji = document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div>h2>a').innerText;
	t = '<br/>'+document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(6)').innerText;
	m = '<br/>'+document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(5)').innerText;
	p = '<br/>'+document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(4)').innerText;
	len = document.querySelectorAll('.newcomp-winning-table>ul>li').length;
	for(var i=3;i<len+1;i++){
		sel = '.newcomp-winning-table>ul>li:nth-child('+i+')>div>h2>a';
		yeji = yeji + '<br/>' + document.querySelector(sel).innerText;
		sel_t = '.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(6)';
		t = t + '<br/>' + document.querySelector(sel_t).innerText;
		sel_m = '.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(5)';
		m = m + '<br/>' + document.querySelector(sel_m).innerText;
		sel_p = '.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(4)';
		p = p + '<br/>' + document.querySelector(sel_p).innerText;
		// var para = document.createElement("div");
		// var node = document.createTextNode(yeji);
		// element = document.querySelector(".newcomp-winning-table");
		// para.appendChild(node);
		// element.appendChild(para);
	}
	// document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(1)').innerText = yeji
	document.write(yeji);
	document.write(t);
	document.write(m);
	document.write(p);
}
getYeji()



function getQyzz(){
	qyzz = document.querySelector(".newcomp-winning-table>ul>li:nth-child(2)>div>h2>a").innerText;
	len = document.querySelectorAll(".newcomp-winning-table>ul>li").length;
	for(var i=2;i<=len;i++){
		sel = ".newcomp-winning-table>ul>li:nth-child("+i+")>div>h2>a";
		qyzz = qyzz + '\n' + document.querySelector(sel).innerText;
	}
	document.querySelector(".newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(3)").innerText = qyzz;
	console.log(qyzz)
}
getQyzz()

function getxmjlyej(){
	yeji = ''
	t = ''
	lenthli = document.querySelectorAll('.newcomp-winning-table>ul>li').length
	for(var i=2;i<lenthli+1;i++){
		yeji += '<br/>' + document.querySelector('.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(2)>h2>a').innerText
		t += '<br/>' + document.querySelector('.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(5)').innerText
	}
	document.write(yeji)
	document.write(t)
}
getxmjlyej()
