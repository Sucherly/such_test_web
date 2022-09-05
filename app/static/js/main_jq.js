$(function(){
    // 添加全局请求头
    $.ajaxSetup({
        global:true,
        timeout:10000,
        beforeSend:function(XMLHttpRequest,settings){
            XMLHttpRequest.setRequestHeader('authorization', localStorage.getItem("token"))

        },
        complete:function(XMLHttpRequest,textStatus){
            var sessionstatus = XMLHttpRequest.getResponseHeader("sessionstatus");
            var status  = XMLHttpRequest.status;
            var readyState  = XMLHttpRequest.readyState;
            console.log(status);
            console.log(textStatus);
            console.log(this.url)
            if(status!=200 && this.url.indexOf("/api/login")<=0 &&this.url!="/api/login" &&this.url!="/api/register" && !localStorage.getItem("name")){
                alert("请先登录！");
                location.href="/";
            }
            if(status=405){

            }
        },
        error:function(xhtp,info){
            console.log(xhtp);
            let data=xhtp.responseJSON;
            alert(data.msg);
            // location.href="/";
            },
    })

// 检测cookie以设置storage
if(!getCookie('token')){
   //清除
   localStorage.clear();
}
//导航条active显示
let loc_pre=location.host
let path=location.pathname

$("#navbarSupportedContent > ul >li").each(function(index,element){
    let arr=element.querySelector('a').href.split(loc_pre);
    let ele_href=arr[1].indexOf('#')<=0?arr[1]:element.id;
    console.log('路径为：'+ele_href);
    if(ele_href=='/'){
        path==ele_href?element.classList.add("active"):element.classList.remove("active");
    }
    else{
        path.indexOf(ele_href)>=0?element.classList.add("active"):element.classList.remove("active");
    }
})
let username_ele;
//登录注册按钮显示
if(localStorage.getItem("token")){
    $("#login_div").hide();
    $("#logout").show();
    username_ele=$("#username");
    username_ele.show();
    console.log(localStorage.getItem("name"));
    username_ele.children('a').text(localStorage.getItem("name").replace('"','').replace('"',''));
}
else{
    $("#login_div").show();
    username_ele=$("#username");
    username_ele.hide()
    username_ele.text("")

}
//登录注册框显示
$('#loginModal').on('shown.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let btn_text=button.data('whatever');

    if(btn_text=='login'){
        if($('#inputPassword2')){
            $('#inputName').parent().hide();
            $('#inputPassword2').parent().hide();
        }
        $("#loginForm").attr('name','login');
    }
    else{
        if($('#inputPassword2')){
            $('#inputName').parent().show();
            $('#inputPassword2').parent().show();
        }
        else{
            alert('页面显示不全！');
        }
        $("#loginForm").attr('name','register');
    }
    $("#loginModalLabel").text(button.text());
});

// 注册登录
$("#loginForm").submit(function(e){
    e.preventDefault();
    let this_form=$("#loginForm");
    let value = this_form.serializeArray();
    let form_data={}
    $.each(value, function (index, item) {
        form_data[item.name] = item.value;
    });
    let form_name=this_form.attr('name')
    let url=form_name=="login"?"login":"register";
    let json = JSON.stringify(form_data);
    console.log("注册登录提交数据"+json);
    $.ajax({
        url:"/api/"+url,
        type:"POST",
        dataType: "json",
        contentType:"application/json",
        data:json,
        success:function(data){
            console.log("登录接口状态"+data);
            
            if(data.code==200){
                console.log("200"+data);
                alert("登录成功！");
                let token=JSON.stringify(data.token);
                localStorage.setItem("token",token);
                localStorage.setItem("name",JSON.stringify(data.data.username));
                setCookie("token",token)
                location.reload();
            }
            else{
                console.log("others:");
                console.log(data);
                alert(data);
                location.href="/";
            }
            
        },
        
    });
});
//退出
$("#logout").on("click",function(){
    console.log(location.href);
    $.ajax({
        url: "/api/logout",
        type: "GET",
        dataType: "json",
        success: function(data) {
            localStorage.clear();
            location.href="/";
        }
    });
});

// 产品接口下拉菜单显示
$("#product_api").click(function(){
    $("#production_dropdown").empty();
    $.ajax({
        url:"/api/productions",
        type:"GET",
        dataType:"json",
        success:function(data){
            for (k in data.data){
                console.log(data.data[k]);
                dt=data.data[k];
                let ele = document.createElement("a");
                ele.className="dropdown-item";
                ele.href="/product_api/product="+dt.id;
                ele.innerHTML=dt.name;
                $("#production_dropdown").append(ele)
            }
        }
    });

});


//左侧垂直导航条显示
$('#myTab a').on('click', function (event) {
  event.preventDefault()
  $('#myTab a').each((i,ele) => ele.classList.remove("active"));
  $(this).addClass('active');
});
// 产品selection的option设置
if($("#inputProduct").length){
    $.ajax({
        url: "/api/productions",
        type: "GET",
        dataType: "json",
        success: function(data) {
            let res=data.data
            let product_select=$("#inputProduct")
            for(i=0;i<res.length;i++){
                let dt=res[i];
                let op_ele=document.createElement('option')
                op_ele.value=dt.id;
                op_ele.text=dt.name;
                product_select.append(op_ele);
            }
        }
    });
}

$('div[class$=".code"]').each(el => {
  // then highlight each
  hljs.highlightElement(el);
});
});

 //获取cookie
 function getCookie(name) {
     let nameEQ = name + "=";
     console.log("cookie:");
     console.log(document.cookie);
   let ca = document.cookie.split(';'); //把cookie分割成组
   for (let i = 0; i < ca.length; i++) {
     let c = ca[i]; //取得字符串
     while (c.charAt(0) == ' ') { //判断一下字符串有没有前导空格
       c = c.substring(1, c.length); //有的话，从第二位开始取
   }
     if (c.indexOf(nameEQ) == 0) { //如果含有我们要的name
       return unescape(c.substring(nameEQ.length, c.length));; //解码并截取我们要的值
   }
}
return false;
}
 //设置cookie
 function setCookie(name, value, seconds) {
 seconds = seconds || 0;   //seconds有值就直接赋值，没有为0
 var expires = "";
 if (seconds != 0) {      //设置cookie生存时间
     var date = new Date();
     date.setTime(date.getTime() + (seconds * 1000));
     expires = "; expires=" + date.toGMTString();
 }
 document.cookie = name + "=" + escape(value) + expires + "; path=/";   //转码并赋值
}