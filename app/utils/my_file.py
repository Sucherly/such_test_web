import os
import shutil
from datetime import datetime

from config import config


class MyFile:
    @staticmethod
    def choose_latest_file(dir_path, key='.html', files_num=1):
        """根据名称关键字选择文件"""
        all_files = os.listdir(dir_path)
        files = [dt for dt in all_files if os.path.isfile(os.path.join(dir_path, dt)) and key in dt]
        files_sort = sorted(files)
        return [os.path.join(dir_path, dt) for dt in files_sort[-files_num::]]

    @staticmethod
    def get_upload_folder():
        """设置上传文件目录"""
        if not config.UPLOAD_FOLDER:
            config.UPLOAD_FOLDER = r"C\such_test_web\upload"
            os.makedirs(r"C\such_test_web\upload")
        return config.UPLOAD_FOLDER

    @staticmethod
    def get_download_folder():
        """设置下载文件目录"""
        if not config.DOWNLOAD_FOLDER:
            config.DOWNLOAD_FOLDER = r"C\such_test_web\download"
            os.makedirs(r"C\such_test_web\download")
        return config.DOWNLOAD_FOLDER

    @staticmethod
    def copy_file(old_file, new_name, new_path):
        """另存为新文件"""
        if not os.path.exists(old_file):
            raise EnvironmentError("{}不存在".format(old_file))
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        suffix = os.path.splitext(old_file)[-1]
        new_file_path = os.path.join(new_path, new_name + now + suffix)  # 新文件名称
        shutil.copy(old_file, new_file_path)  # 复制文件
        return os.path.abspath(new_file_path)
