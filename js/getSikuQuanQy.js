function getSikuQuanQy(){
	qiye = document.querySelector('.scTable .el-table__body-wrapper tbody>tr:nth-child(1)>td:nth-child(3) span').innerText
	len = document.querySelectorAll('.scTable .el-table__body-wrapper tbody>tr').length
	for(var i=2;i<len+1;i++){
		sel = '.scTable .el-table__body-wrapper tbody>tr:nth-child('+i+')>td:nth-child(3) span'
		qiye = qiye + '\n' + document.querySelector(sel).innerText
	}
	document.querySelector('.scTable .el-table__body-wrapper tbody>tr:nth-child(1)>td:nth-child(2) div').innerText = qiye
	// document.write(qiye)
}
getSikuQuanQy()

function getSikuQuanQyzz(){
	qyzz = ''
	len = document.querySelectorAll('#pane-companyQuality .el-table__body-wrapper>table.el-table__body>tbody>tr').length
	for(var i=1;i<len;i++){
		// sel = "#pane-companyQuality tbody>tr:nth-child("+i+")>td:nth-child(4)>div"
		qyzz += '\n'+document.querySelector('#pane-companyQuality tbody>tr:nth-child('+i+')>td:nth-child(4)>div').innerText
	}
	document.querySelector("#pane-companyQuality tbody>tr:nth-child(1)>td:nth-child(2)>div").innerText = qyzz
}
getSikuQuanQyzz()