# git 仓库地址
https://github.com/Sucherly/such_test_web.git
# git 加速
https://fhefh2015.github.io/Fast-GitHub/
<br>
在浏览器中打开该地址,下载本浏览器对应的插件

# 本项目简介
本项目由Sucherly独立开发的开源项目，旨在为自动化测试服务。

# 本项目目录
-document  # 使用手册<br>
--document_ch  # 中文版使用手册<br>
--document_en  # 英文版使用手册<br>

# 本项目环境搭建
## python 安装
## pip 安装第三方库
```commandline
pip install flask --default-timeout=10000
pip install flask-Migrate --default-timeout=10000
pip install flask-Moment --default-timeout=10000
pip install flask-SQLAlchemy --default-timeout=10000
pip install flask-httpauth --default-timeout=10000
pip install flask_apscheduler --default-timeout=10000
pip install flask_login --default-timeout=10000
pip install authlib --default-timeout=10000
pip install python-dotenv --default-timeout=10000
pip install flask-cors --default-timeout=10000
pip install bootstrap4 --default-timeout=10000

注意安装完成后检查下werkzeug的版本是否与flask版本一致
```
## node
下载地址：https://nodejs.org/zh-cn/download/
## npm 安装第三方库
```commandline
npm install -g create-react-app
```
（创建应用create-react-app "C:\python project\such_test_web\frontend"）

# 本项目构建

```commandline
cd C:\python project\such_test_web\frontend
npm start
npm run build
```