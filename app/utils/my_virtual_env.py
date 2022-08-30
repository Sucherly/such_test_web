import os


class MyVirtualEnv:
    def __init__(self, local_dir, env_name='venv'):
        self.local_dir = local_dir
        self.disk = self.local_dir.split(':')[0]  # 目录所在盘
        self.env_name = env_name

    def switch_to_dir(self):
        """进入目录"""
        os.popen(self.disk + ':')
        os.popen('cd ' + self.local_dir)

    def env_create(self):
        """创建虚拟环境"""
        os.popen('virtualenv ' + self.env_name)

    @staticmethod
    def env_active():
        """激活虚拟环境"""
        os.popen('activate')

    @staticmethod
    def env_deactivate():
        """退出虚拟环境"""
        os.popen('deactivate')

    def env_create_with_name(self):
        """创建虚拟环境"""
        os.popen('mkvirtualenv ' + self.env_name)

    def env_active_with_name(self):
        """激活虚拟环境"""
        os.popen('workon ' + self.env_name)

    def env_deactivate_with_name(self):
        """退出虚拟环境"""
        os.popen('deactivate ' + self.env_name)

    def env_remove_with_name(self):
        """删除虚拟环境"""
        os.popen('rmvirtualenv ' + self.env_name)

    def env_into_dir_with_name(self):
        """进入虚拟环境目录"""
        os.popen('cdvirtualenv ' + self.env_name)

    @staticmethod
    def envs_list():
        """列出虚拟环境"""
        os.popen('lsvirtualenv ')

    def create_active_env(self):
        """创建并激活虚拟环境"""
        self.switch_to_dir()  # 进入目录
        self.env_create()  # 创建目录
        self.env_active()  # 激活目录

    def create_active_env_with_name(self):
        """创建并激活虚拟环境"""
        self.switch_to_dir()  # 进入目录
        self.env_create_with_name()  # 创建目录
        self.env_active_with_name()  # 激活目录
