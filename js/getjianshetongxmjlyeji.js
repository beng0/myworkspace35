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