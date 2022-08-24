if (window.XMLHttpRequest)
{
    //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
}
else
{
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
//  IE7+, Firefox, Chrome, Opera, Safari 浏览器使用XMLHttpRequest，IE6, IE5 浏览器使用ActiveXObject
//if (window.XMLHttpRequest) xmlhttp=new XMLHttpRequest() else xmlhttp=new ActiveXObject("Microsoft.XMLHTTP")

function productions(){
xmlhttp.open("GET","/api/productions",true);
xmlhttp.send();
xmlhttp.onreadystatechange=function()
{
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        data=xmlhttp.responseText;
        let production_dropdown=document.getElementById("production_dropdown");
        for (k in data.data){
            dt=data.data[k];
            let ele = document.createElement("a");
            ele.className="dropdown-item";
            ele.href="/api/productions/"+dt.id;
            ele.innerHTML=dt.name;
            production_dropdown.appendChild(ele)
        }

    }

}
}


