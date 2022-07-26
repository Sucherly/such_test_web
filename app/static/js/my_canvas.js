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

function draw_logo_text(ctx,x,y,top,color=['#4B0082','#4682B4','#483D8B','#D8BFD8','#87CEEB','#E6E6FA','#D8BFD8']){
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