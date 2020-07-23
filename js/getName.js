function getName(){
	name = document.querySelector('.newcomp-winning-table>ul>li:nth-child(2) h2>a').innerText
	len = 16
	for(var i=3;i<len+1;i++){
		sel = '.newcomp-winning-table>ul>li:nth-child('+i+') h2>a'
		name = name + '\n' + document.querySelector(sel).innerText
	}
	document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(1)').innerText = name
}

function getZhuanye(){
	zhuanye = document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(3)>h2').innerText
	len = 16
	for(var i=3;i<len+1;i++){
		sel = '.newcomp-winning-table>ul>li:nth-child('+i+')>div:nth-child(3)>h2'
		zhuanye = zhuanye + '\n' + document.querySelector(sel).innerText
	}
	document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(4)').innerText = zhuanye
}
function getYeji(){
	yeji = document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div>h2>a').innerText
	len = 16
	for(var i=3;i<len+1;i++){
		sel = '.newcomp-winning-table>ul>li:nth-child('+i+')>div>h2>a'
		yeji = yeji + '<br/>' + document.querySelector(sel).innerText
	}
	// document.querySelector('.newcomp-winning-table>ul>li:nth-child(2)>div:nth-child(1)').innerText = yeji
document.write(yeji)
}
getYeji()
getName()
getZhuanye()