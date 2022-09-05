import os

root_dir = os.path.abspath(__file__).split('tests')[0]


def get_migration_dir():
    """获取数据库迁移目录绝对地址"""
    return os.path.join(root_dir, 'migrations')
