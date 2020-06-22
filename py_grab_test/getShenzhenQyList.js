function get_qyList(){
	var url = ''
	for(var j=1;j<=3;j++){
		__doPostBack("ctl00$ContentPlaceHolder1$AspNetPager1",j)
		len_l  = document.querySelectorAll("table.data-list>tbody>tr").length
		for(var i =2;i<=len_l;i++){
			sel1 = "table.data-list>tbody>tr:nth-child("+i+")>td:nth-child(1)>a"
			url_m = document.querySelector(sel1).getAttribute("href")
			url+=url_m
			// var para = document.createElement("div")
			// var node = document.createTextNode(url_m)
			// element = document.querySelector(".wrapper-main>div.container")
			// para.appendChild(node)
			// element.appendChild(para)
		}
	}
	// var para = document.createElement("div")
	// var node = document.createTextNode(url)
	// element = document.querySelector(".wrapper-main>div.container")
	// para.appendChild(node)
	// element.appendChild(para)
	console.log(url)
	
}

get_qyList()

function __doPostBack(eventTarget, eventArgument) {
    theForm.__EVENTTARGET.value = eventTarget;
    theForm.__EVENTARGUMENT.value = eventArgument;
    theForm.submit();
}


var timeout = prompt("设置刷新时间");
current = location.href;
if(timeout > 0)
{
　　setTimeout('reload()', 1000 * timeout);
}
else
{
　　location.replace(current);
}

function reload()
{
　　setTimeout('reload()', 1000 * timeout);
　　var frame = '<frameset cols=\'*\'>\n<frame src=\'' + current + '\' /></frameset>';
　　with(document)
　　{
    // 引用document对象，调用write方法写入框架，打开新窗口
　　　　write(frame);
　　
　　　　//此处输入代执行的代码
　　　　
   // 关闭上面的窗口
　　　　void(close());
　　};
}

function f1(t){
	timeout = t;
	current = location.href;
	if(timeout > 0){
		setTimeout(reload(),1000*timeout)
	}
	else{
		location.replace(current)
	}
}
function reload(current,n)
{

　　var frame = '<frameset cols=\'*\'>\n<frame src=\'' + current + '\' /></frameset>';
　　with(document)
　　{
    // 引用document对象，调用write方法写入框架，打开新窗口
　　　　write(frame);
　　
　　　　console.log("hello")
　　　　
   // 关闭上面的窗口
　　　　void(close());
　　};
	n+=1;
	console.log(n);
}
for(var i=0;i<3;i++){
	setTimeout(reload("https://www.baidu.com",1),1000);
}

function setPage(pagenum){
    document.querySelector("#newpage").value = pagenum
}
setPage(4)
function __doPostBack(eventTarget, eventArgument,pagenum) {
    document.querySelector("#newpage").value = pagenum
    var theForm = document.forms['form1']
    theForm.__EVENTTARGET.value = eventTarget;
    theForm.__EVENTARGUMENT.value = eventArgument;
    theForm.submit();
}
__doPostBack('Linkbutton5','',5)