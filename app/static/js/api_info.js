$(function(){
// 产品接口详情页面
let api_id=$("a[name='name']").attr("data-id");
// api删除
$("#delete_api").on("click",function(){
    $.ajax({
        url:"/api/interface/delete/id="+api_id,
        type: "GET",
        dataType:"json",
        success: function(data){
            alert(data.msg);
            location.href="/product_api/product="+data.data.product;
        }
    });

});

// api编辑弹框显示
$('#apiModal').on('shown.bs.modal', function (event) {
    let button = $(event.relatedTarget);
    $("#api_id").show();
    $.ajax({
        url:"/api/interface/id="+api_id,
        type: "GET",
        dataType:"json",
        success: function(data){


            for(k in data.data){
                console.log(k);
                let ele=$("[name='"+k+"']");
                let tagName=ele.prop("tagName");
                console.log(tagName);
                if(ele.tagName=="select"){
                    $("option[id="+data.data[k]+"]").select();

                }
                else{
                    ele.val(data.data[k]);
                }
                
            }
        }
    });
    
});


});