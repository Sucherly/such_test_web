import logging
import os
from logging import handlers

level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}  # 日志级别关系映射


class MyLogger:
    def __init__(self, filename, level='info', when='D', backCount=3, fmt=None, is_stream_handle=False):
        self.fmt = fmt or '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        self.dir_name = os.path.abspath(os.path.dirname(filename))
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(self.fmt)  # 设置日志格式
        self.logger.setLevel(level_relations.get(level))  # 设置日志级别
        # 往文件里写入
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(th)  # 把对象加到logger里
        if is_stream_handle:
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            self.logger.addHandler(sh)
