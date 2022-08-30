from requests.adapters import HTTPAdapter
import os
from app.logger.logger import MyLogger
from config import config

old_path = os.getcwd()
path = old_path.split(r"test_case")[0]
os.chdir(path)

is_log = config.is_log


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = config.api_timeout  # 单位是秒
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        if is_log:
            self.http_log_info = config.http_log_info  # http输出信息日志。存放正常的接口信息
            self.http_log_conn = config.http_log_conn  # http连接超时日志。存放正常的接口信息
            self.is_headers = config.is_headers  # http_info*.log中是否记录request.header
            self.is_body = config.is_body  # http_info*.log中是否记录request.body
            self.is_response = config.is_response  # http_info*.log中是否记录response
            self.is_stack = config.is_stack  # http_info*.log中是否记录response
            if self.is_stack:
                self.my_logger = MyLogger(self.http_log_info)
            else:
                self.my_logger = MyLogger(self.http_log_info, fmt='%(asctime)s: %(message)s')
            # self.my_logger_conn = MyLogger(self.http_log_conn)
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        response = super().send(request, **kwargs)
        info = '\n--url:{};\n--headers:{};\n--body:{};\n--response:{};\n--request.headers:{}'.format(request.url,
                                                                                                     response.headers,
                                                                                                     request.body or ' ',
                                                                                                     response.text,
                                                                                                     request.headers)
        exc_info = '\n--[接口异常信息开始]--{}--[接口异常信息结束]--\n'.format(info)
        if response.status_code == 200:
            if is_log:
                info_headers = '\n--headers:{};'.format(response.headers) if self.is_headers else ''
                info_body = '\n--body:{};'.format(request.body) if self.is_body else ''
                info_response = '\n--response:{};'.format(response.text) if self.is_response else ''
                request_headers = '\n--request.headers:{};'.format(request.headers) if self.is_response else ''
                normal_info = '\n--url:{};{}{}{}{}'.format(request.url, info_headers, info_headers, info_body,
                                                           info_response, request_headers)
            else:
                normal_info = None
            if str(response.text):
                try:
                    res = response.json()
                    if 'code' in res and res['code'] != 200:
                        print(exc_info)
                    elif is_log:
                        self.my_logger.logger.info(normal_info)
                except ValueError:
                    if is_log:
                        self.my_logger.logger.info(normal_info)
            elif is_log:
                self.my_logger.logger.info(normal_info)
        else:
            print(exc_info)
        return response
