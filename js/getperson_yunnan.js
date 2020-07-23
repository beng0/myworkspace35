function getName(){
	name = document.querySelector('tbody#zcry_table>tr:nth-child(1)>td:nth-child(2)').innerText;
	len = document.querySelectorAll('tbody#zcry_table>tr').length;
	for(var i=2;i<=len;i++){
		sel = 'tbody#zcry_table>tr:nth-child('+i+')>td:nth-child(2)';
		name = name + '\n'+ document.querySelector(sel).innerText
	}
	document.querySelector('tbody#zcry_table>tr:nth-child(1)>td:nth-child(1)').innerText = name
}
getName()
function getZzname(){
	zzname = document.querySelector('tbody#zcry_table>tr:nth-child(1)>td:nth-child(4)').innerText;
	len = document.querySelectorAll('tbody#zcry_table>tr').length;
	for(var i=2;i<=len;i++){
		sel = 'tbody#zcry_table>tr:nth-child('+i+')>td:nth-child(4)';
		zzname = zzname + '\n'+ document.querySelector(sel).innerText
	}
	document.querySelector('tbody#zcry_table>tr:nth-child(1)>td:nth-child(3)').innerText = zzname
}
getZzname()
function getZhuanye(){
	zhuanye = document.querySelector('tbody#zcry_table>tr:nth-child(1)>td:nth-child(6)').innerText;
	len = document.querySelectorAll('tbody#zcry_table>tr').length;
	for(var i=2;i<=len;i++){
		sel = 'tbody#zcry_table>tr:nth-child('+i+')>td:nth-child(6)';
		zhuanye = zhuanye + '\n'+ document.querySelector(sel).innerText
	}
	document.querySelector('tbody#zcry_table>tr:nth-child(1)>td:nth-child(5)').innerText = zhuanye
}
getZhuanye()
