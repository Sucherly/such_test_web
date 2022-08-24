$(function(){
// 产品页面显示
$.ajax({
    url: "/api/productions",
    type: "GET",
    dataType: "json",
    success: function(data) {

        let res=data.data
        console.log(res);
        for(i=0;i<res.length;i++){
            let dt=res[i];
            let div_ele=document.createElement('div')
            div_ele.classList.add("card");

            let img_ele=document.createElement('img')
            img_ele.classList.add("card-img-top");
            img_ele.setAttribute("alt","...");
            img_ele.setAttribute("src","../static/images/1.jpg");
            div_ele.appendChild(img_ele);

            let div_ele1=document.createElement('div')
            div_ele1.classList.add("card-body");

            let h=document.createElement('h5')
            h.classList.add("card-title");
            let a=document.createElement("a");
            a.href="/product_api/product="+dt.id
            a.text=dt.name
            h.appendChild(a);
            let p=document.createElement('p')
            p.classList.add("card-text");
            p.append(dt.description);

            div_ele1.appendChild(h);
            div_ele1.appendChild(p);

            div_ele.appendChild(div_ele1);
            $("#production_cards").append(div_ele);
        }
    }
});

});