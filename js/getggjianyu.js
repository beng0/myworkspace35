function getgg(){
	gg = ''
	t = ''
	lis = document.querySelectorAll('.lucene>ul>li')
	lenthli = lis.length
	for(var i=1;i<lenthli;i++){
		sel = '.lucene>ul>li:nth-child('+i+')>div>div:nth-child(1)>div>a'
		sel_t = '.lucene>ul>li:nth-child('+i+')>div>div:nth-child(2)>span'
		gg += '</br>'+document.querySelector(sel).innerText
		t += '</br>'+document.querySelector(sel_t).innerText
	}
	document.write(gg+t)
}
getgg()