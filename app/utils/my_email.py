import os
import smtplib
import zipfile
from datetime import datetime
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MyEmail:
    """邮件发送"""

    def __init__(self, smtp_server, sender, sender_pwd, receiver):
        self.smtp_server = smtp_server  # 邮箱服务器
        self.sender = sender  # 发件人邮箱
        self.sender_pwd = sender_pwd  # 发件人密码
        self.receiver = ','.join(receiver) if isinstance(receiver, list) else receiver  # 收件人邮箱
        self.server = None
        self.sender_login()
        self.mail = MIMEMultipart()
        self.mail['From'] = self.sender
        self.mail['To'] = self.receiver

    def sender_login(self):
        """发件人登录邮箱"""
        self.server = smtplib.SMTP(self.smtp_server)
        self.server.login(self.sender, self.sender_pwd)

    def mail_subject(self, content=''):
        self.mail['Subject'] = content

    def mail_body(self, content):
        self.mail.attach(MIMEText(content, 'plain', 'utf-8'))

    def mail_files(self, files):
        """邮件添加附件--直接添加，不压缩"""
        for file in files:
            filename = os.path.basename(file)
            att = MIMEApplication(open(file, 'rb').read())  # 用二进制读附件
            att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
            self.mail.attach(att)

    def mail_zip_files(self, files):
        """邮件添加附件--压缩文件"""
        now_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = 'ZIPFiles_{}.zip'.format(now_time)
        dir_name = r'C:\such_test_web\report_zip'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        zip_path = os.path.join(dir_name, filename)
        zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            name = os.path.basename(file)
            zip.write(file, arcname=name)
        zip.close()
        with open(zip_path, 'rb') as f:
            att = MIMEBase('zip', 'zip', filename=filename)
            att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', filename))
            att.add_header('Content-ID', '<0>')
            att.add_header('X-Attachment-Id', '0')
            att.set_payload(f.read())
            encoders.encode_base64(att)
            self.mail.attach(att)

    def send(self):
        self.server.sendmail(self.sender, self.receiver, self.mail.as_string())
        self.server.quit()
