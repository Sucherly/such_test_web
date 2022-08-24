$(function(){
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
    console.log(json);
    $.ajax({
        url:"/api/"+url,
        type:"POST",
        dataType: "json",
        contentType:"application/json",
        data:json,
        success:function(data){
            localStorage.setItem("token",JSON.stringify(data.token));
            localStorage.setItem("name",JSON.stringify(data.data.username));
            location.reload();
        }
    });
});
//退出
$("#logout").on("click",function(){
    $.ajax({
        url: "/api/logout",
        type: "GET",
        dataType: "json",
        success: function(data) {
            localStorage.clear();
            location.reload();
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