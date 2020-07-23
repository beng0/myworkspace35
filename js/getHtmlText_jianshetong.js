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

