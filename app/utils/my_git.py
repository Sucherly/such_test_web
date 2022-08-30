import os
import traceback
from git.repo import Repo
from git.repo.fun import is_git_dir
from werkzeug.exceptions import abort


class MyGit:
    def __init__(self, git_url, git_username=None, git_password=None, SSHKey=None):
        self.git_url = git_url
        if 'http' in git_url:
            if not git_username or not git_password:
                git_username = os.getenv('GIT_USERNAME')
                git_password = os.getenv('GIT_PASSWORD')
            if not git_username or not git_password:
                abort(500, 'git用户名或密码为空！请先维护！')
            os.environ['GIT_USERNAME'] = git_username
            os.environ['GIT_PASSWORD'] = git_password
            os.popen('$ git config user.name' + git_username)
            os.popen('$ git config user.password ' + git_password)

    def initial(self, to_path, branch='master'):
        """初始化仓库"""
        # to_path不存在时，创建目录
        if not os.path.exists(to_path):
            try:
                os.makedirs(to_path)
            except Exception as e:
                traceback.format_stack(e)
        git_local = os.path.join(to_path, '.git')
        # 判断to_path目录是不是git仓库
        if not is_git_dir(git_local):
            repo = Repo.clone_from(self.git_url, to_path=to_path, branch=branch)  # 拉取代码
        else:
            repo = Repo(to_path)  # 直接使用现有仓库
        return repo

    def pull(self, repo):
        """拉最新代码"""
        repo.git.pull()

    def reset(self, repo, *args):
        """reset"""
        repo.git.reset(args)

    def branches(self, repo):
        """
        获取所有分支
        :return:
        """
        branches = repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]

    def tags(self, repo):
        """获取所有tag(版本)"""
        return [tag.name for tag in repo.tags]

    def change_to_branch(self, repo, branch):
        """切换分支"""
        repo.git.checkout(branch)

    def change_to_commit(self, repo, branch, commit, type='--hard'):
        """切换分支后commit
        ：参数：
        - type:commit方式，默认强制（--hard）
        """
        self.change_to_branch(repo, branch)
        repo.git.reset(type, commit)

    def change_to_tag(self, repo, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        repo.git.checkout(tag)
