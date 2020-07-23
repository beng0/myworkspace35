function formSubmit(){
	
}
formSubmit()
var topwin = window.top.document.getElementById("newsiframe").contentWindow;
topwin.document.querySelector("#page").value = "12";
topwin.document.forms[0].submit();

var topwin = window.top.document.getElementById("newsiframe").contentWindow;
topwin.document.querySelector("div.news_con").innerHTML
