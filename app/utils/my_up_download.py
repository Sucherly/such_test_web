import os
from app.utils.my_file import MyFile


class MyUpDownload:
    def __init__(self, allowed_extensions=None):
        self.allowed_extensions = allowed_extensions or (
            'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jpeg', 'rar', 'doc', 'docx', 'dot', 'pptx', 'db',
            'xlsx', 'html')  # 允许的格式,保证安全性

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.allowed_extensions

    def upload_file(self, file):
        """上传文件"""
        if file and self.allowed_file(file.filename):
            filename = file.filename  # 文件名,支持中文哦！！！
            filename = str(filename)  # 防止恶意传送非正常字符导致服务器异常
            path = os.path.join(MyFile.get_upload_folder(), filename)
            file.save(path)
            return path
        return ''

    @staticmethod
    def download_file(self, filename):
        """下载文件"""
        filepath = os.path.join(MyFile.get_download_folder(), filename)
        if filepath:
            # return send_file(filepath, attachment_filename=filename)
            pass
            # return app.send_static_file(filepath)
        return ''
