$(function(){
// 产品接口页面
// 左侧ul显示
let path=unescape(location.pathname);
let product_id=path.split('/product=');
product_id=product_id[product_id.length-1]
// $.ajax({
//     url: "/api/production/product="+product_id,
//     type: "GET",
//     dataType: "json",
//     success: function(data) {
//         let res=data.data
//         let a_ele=$("#product_nav > nav > ol > li > a");
//         a_ele.text(res.name);
//         a_ele.attr("href","/product_api/product="+res.id);
//     }
// });
// 接口列表显示
$.ajax({
    url: "/api/interfaces/product="+product_id,
    type: "GET",
    dataType: "json",
    success: function(data) {

        let res=data.data
        let keys=["name","url","description","version","status","request_type"]
        let status=["启用","已弃用","未完全弃用"]
        // 表格
        let tbody=$("#apiTable > table > tbody");
        for(i=0;i<res.length;i++){
            let dt=res[i];
            let tr_ele=document.createElement('tr')
            $.each(keys,function(idx){
                k=keys[idx];
                let td_ele=document.createElement('td');
                let text=k=="status"?status[dt[k]]:dt[k];
                let text_ele;
                if(k=="name"){
                    text_ele=document.createElement('a')
                    text_ele.text=text;
                    text_ele.href="/product_api/id="+dt.id;
                }
                else{
                    text_ele=document.createTextNode(text);
                }
                
                td_ele.appendChild(text_ele);
                tr_ele.appendChild(td_ele);
            })
            // 查看测试代码按钮
            let td_ele=document.createElement('td');
            let bt_ele=document.createElement('button');
            bt_ele.append("查看测试代码");
            bt_ele.setAttribute("class","btn second_bgColor");
            bt_ele.setAttribute("data-toggle","modal");
            bt_ele.setAttribute("data-target","#apiTestCode");
            bt_ele.setAttribute("data-whatever",dt.id);
            td_ele.appendChild(bt_ele);
            tr_ele.appendChild(td_ele);
            // 运行按钮
            td_ele=document.createElement('td');
            bt_ele=document.createElement('button');
            bt_ele.append("运行");
            bt_ele.setAttribute("class","btn green_bg");
            bt_ele.setAttribute("data-toggle","modal");
            bt_ele.setAttribute("data-target","#apiRunCode");
            bt_ele.setAttribute("data-whatever",dt.id);
            td_ele.appendChild(bt_ele);
            tr_ele.appendChild(td_ele);
            tbody.append(tr_ele);
        }
    }
});

// api新增框显示
$('#apiModal').on('shown.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    $("option[id="+product_id+"]").select();
});
// 查看测试代码框显示
$('#apiTestCode').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget); // 出发该模态框的button
    let api_id = button.data('whatever');
    let modal = $(this)
    let modal_bd=modal.find(".modal-body");
    modal_bd.empty();
    modal_body=modal_bd;
    // let pre=document.createElement("pre");
    // let modal_body=document.createElement("code");
    // let modal_body=modal_bd;
    $.ajax({
        url:"/api/interface/id="+api_id,
        type: "GET",
        dataType:"json",
        success: function(data){
            let dt=data.data;
            let fun="<pre>\n<code>\n"
            //写入标题
            let funcName="def "+dt.name+"(self, "+dt.request_params+"):";
            fun+=funcName
            fun+="\n    "
            // 写入描述
            fun+='"""'+dt.description+'"""'
            fun+="\n    "
            // 写入url
            let url="";
            if(dt.request_params){
                console.log(dt.url.lastIndexOf('/'));
                url=dt.url.slice(0,dt.url.lastIndexOf('/')+1);
                console.log(url);
                let arry=dt.request_params.split(",");
                for(i in arry){
                    let param=arry[i].split(":")[0];
                    console.log(param);
                    url=url+param+"="+param;
                }
            }
            else{
                url=dt.url
            }
            fun+="url = '{}"+url+"'.format(self.base_url)"
            fun+="\n    "
            // 写入headers
            fun+="headers = {}"
            fun+="\n    "
            // 写入body
            fun+="payload = {}"
            fun+="\n    "
            // 写入请求
            fun+="response = requests.request('GET', url=url, headers=headers, params=payload)"
            fun+="\n    "
            // 写入返回
            fun+="return response.json()"
            fun+="</code>\n</pre>"
            modal_body.html(fun);
        }
    });
    // pre.appendChild(modal_body);
    // modal_bd.append(pre);


})
// 运行框显示
$('#apiRunCode').on('show.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    let form=$("#runTestForm");
    form.attr("data-id",button.data('whatever'))
    if(product_id==1){
        form.find("input[name='url']").val(location.protocol+"//"+location.host);
    }

})
// 运行表单提交
$("#runTestForm").submit(function(e){
    e.preventDefault();
    let this_form=$("#runTestForm");
    let value = $('#runTestForm').serializeArray();
    let form_data={}
    $.each(value, function (index, item) {
        form_data[item.name] = item.value;
    });
    let data_id=this_form.attr("data-id");
    form_data.id=data_id
    let json = JSON.stringify(form_data);
    console.log(json);
    $.ajax({
        url:"/api/interface/run",
        type:"POST",
        dataType: "json",
        contentType:"application/json",
        data:json,
        success:function(data){
            // 显示结果
            $("#apiRunCode").hide();
            console.log(data);
            $("#status").append(data.code);
            $("#message").append(data.msg);
            $("#response").append(data.data);
            $("#apiResultShow").attr("class","modal fade show");
            $("#apiResultShow").attr("style","display: block; padding-right: 17px;");
            $("#apiResultShow").attr("role","dialog");
            $("#apiResultShow").attr("aria-hidden","false");
        },
        error:function(xhr){
            alert(xhr.status + "\n" + xhr.statusText);
        },
    });
});
//
// 未关联button的模态框关闭
$('button[name="close_btn"').on('click', function () {
  let modal=$(this).parent().parent().parent().parent();
  modal.attr("class","modal fade");
  modal.attr("style","");
  modal.attr("role","dialog");
  modal.attr("aria-hidden","true");
  modal.hide()
  $(".modal-backdrop").remove();
})
//复制
$("div.bd-clipboard > button").on("click",function(){
    console.log("点击复制按钮")
    let ele=$(this).parent().next().find("code");
    if(ele){
        navigator.clipboard.writeText(ele.html().replaceAll("<br>","\n").replaceAll(" "," "));
    }

});

});