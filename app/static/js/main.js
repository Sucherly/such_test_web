window.onload=function(){
  draw_logo();
  setInterval(function(){draw_background();},1000/3);
  // draw_background();
}
function draw_s(ctx,x,y,r,color){
  ctx.beginPath();
  let x1=r*Math.sin(Math.PI*0.05);
  let y1=r*Math.cos(Math.PI*0.05);
  ctx.moveTo(x-x1,y+y1);
  ctx.arc(x, y, r, Math.PI*0.55, Math.PI*1.8, false);
  ctx.moveTo(x-x1,y+y1);
  y=y+2*r;
  ctx.arc(x, y, r, Math.PI*1.45, Math.PI*0.8, false);
  ctx.strokeStyle=color;
  ctx.lineWidth=2;
  ctx.stroke();
  return y
}

function draw_logo_text(ctx,x,y,top,color=['#4B0082','#4682B4','#483D8B','#D8BFD8','#87CEEB','#A9A9F5','#D8BFD8']){
  let d=10;
  let r=5;
  let [color1,color2,color3,color4,color5,color6,color7]=color
  // 绘制S
  y=draw_s(ctx,x,y,r,color1);
  // 绘制A
  ctx.beginPath();
  x1=x+r+2*d
  ctx.moveTo(x1,y-3*r);
  ctx.lineTo(x1-10,y+r)
  ctx.moveTo(x1,y-3*r);
  ctx.lineTo(x1+10,y+r);
  ctx.strokeStyle=color2;
  ctx.lineWidth=2;
  ctx.stroke();

  // 绘制C
  ctx.beginPath();
  x=x1+10+d+r;
  y=y-r;
  r=2*r;
  x1=r*Math.sin(Math.PI*0.25);
  y1=r*Math.cos(Math.PI*0.25);
  ctx.moveTo(x+x1,y-y1);
  ctx.arc(x, y, r, Math.PI*1.75, Math.PI*0.25, true);
  ctx.strokeStyle=color3;
  ctx.lineWidth=2;
  ctx.stroke();

  // 绘制T
  ctx.beginPath();
  ctx.moveTo(d,top-5);
  ctx.lineTo(x+6*r+2*d,top-5);
  ctx.moveTo(x+2*r,top-5);
  ctx.lineTo(x+r,y+2*r);
  ctx.strokeStyle=color4;
  ctx.lineWidth=4;
  ctx.stroke();
  // 绘制e
  ctx.beginPath();
  x=x+2*r
  r=r/1.5
  ctx.moveTo(x,y);
  x=x+r
  ctx.arc(x, y, r, 0, Math.PI*0.25, true);
  ctx.moveTo(x+r,y);
  ctx.lineTo(x-r,y);
  ctx.strokeStyle=color5;
  ctx.lineWidth=2;
  ctx.stroke();
  // 绘制s
  r=r/2
  x=x+r+d;
  y=y-r
  y=draw_s(ctx,x,y,r,color6);
  // 绘制/
  ctx.beginPath();
  ctx.moveTo(x+2*r+d,top-5);
  ctx.lineTo(x+2*r+d,y+4*r);
  ctx.strokeStyle=color7;
  ctx.lineWidth=3;
  ctx.stroke();
}

function draw_logo(){
  let canvas = document.getElementById('logo');

  if (canvas.getContext){
    let ctx = canvas.getContext('2d');
    var img = new Image();   // 创建一个<img>元素
    img.src = '../static/images/logo.png'; // 设置图片源地址
    img.onload = function(){
      ctx.drawImage(img,0,0,45,45);
    }
    let top;
    let x;
    let y;
    // 绘制文字阴影
    top=10;
    x=42;
    y=20;
    draw_logo_text(ctx,x,y,top,['#DCDCDC'])
    // 绘制文字
    top=10;
    x=40;
    y=20;
    draw_logo_text(ctx,x,y,top)

  } else {
  // canvas-unsupported code here
}
}

// 绘制背景
function draw_background(){
  let canvas=document.getElementById('canvas_back');
  // 设置画面宽高
  canvas.width=window.screen.availWidth-12;
  canvas.height=window.screen.availHeight-50;
  if (canvas.getContext){
    let ctx = canvas.getContext('2d');
    // 绘制渐变背景色
    let grade = ctx.createLinearGradient(0,0,0, canvas.height);
    grade.addColorStop(1, '#7AB5D3');
    grade.addColorStop(0, '#E2F4F9'); 
    ctx.fillStyle=grade;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // 绘制logo符号，随机取符合间隔限制的x,y
    let d=40 // 符号之间的最小间隔
    let x_arry=[];
    let y_arry=[];
    for(let i=0;i<50;i++){
      for(let j=0;j<100;j++){
        let x=Math.floor(Math.random()*canvas.width);
        let y=Math.floor(Math.random()*canvas.height);
        let flag_x=true;
        let flag_y=true;
        for(dt in x_arry){
          if(Math.abs(x-x_arry[dt])<d){
            flag_x=false
            break;
          }
        }
        for(dt in y_arry){
          if(Math.abs(y-y_arry[dt])<d){
            flag_y=false
            break;
          }
        }
        if(flag_x || flag_y){
          draw_cs(ctx,x,y);
          x_arry.push(x);
          y_arry.push(y);
          break;
        }
      }
    }
    // 定时
    ctx.save();
    ctx.rotate(2);
    ctx.translate(105,0);
    ctx.translate(0,28.5);
    ctx.restore(); 
  };
  
}

// 绘制logo符号
function draw_cs(ctx,x,y){
  let r=20;
  ctx.beginPath();
  x1=r*Math.sin(Math.PI*0.1);
  y1=r*Math.cos(Math.PI*0.1);
  ctx.moveTo(x+x1,y-y1);
  ctx.arc(x, y, r, Math.PI*1.6, Math.PI*0.5, true);
  // ctx.strokeStyle="#c7eae8";
  ctx.strokeStyle="#c7eae8";
  ctx.lineWidth=2;
  ctx.stroke();
  draw_s(ctx,x-2,y-r/2,r/2,"#c7eae8");
  

}
//IE7+, Firefox, Chrome, Opera, Safari 浏览器使用XMLHttpRequest，IE6, IE5 浏览器使用ActiveXObject
let xmlhttp=window.XMLHttpRequest?new XMLHttpRequest():new ActiveXObject("Microsoft.XMLHTTP");

function productions_dropdown(){
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




window.addEventListener("load", function () {
  function sendData(url){
  // 我们把这个 FormData 和表单元素绑定在一起。
  let FD  = new FormData(form);
  let objData = {}
  FD.forEach((v, k) => {objData[k] = v})
  let jd = JSON.stringify(objData)
  console.log(jd);

    // 我们定义了数据成功发送时会发生的事。
    xmlhttp.addEventListener("load", function(event) {
      var data=JSON.parse(event.target.responseText);
      alert(data.msg);
      location.reload();
    });

    // 我们定义了失败的情形下会发生的事
    xmlhttp.addEventListener("error", function(event) {
      alert(event.target.responseText);
    });

    // 我们设置了我们的请求
    xmlhttp.open("POST", url);
    // 发送的数据是由用户在表单中提供的
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.send(jd);
  };

  // 创建产品接口表单提交
  var form = document.getElementById("apiForm");
  if(form){
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      let url="productAPI";
      sendData("/api/"+url);
    });
  }
  
});