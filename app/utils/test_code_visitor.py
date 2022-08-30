import ast
import os
from threading import Thread

# ----------------
# ast遍历python test cases源代码
# ----------------


class TestCodeVisitor:
    def __init__(self):
        self.testFile_list = []
        self.pageFile_list = []
        self.tests = {}
        self.pages = {}
        self.exceptFileName = []

    def get_file_list(self, root_path):
        """获取所有page文件路径、test文件路径"""
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file in self.exceptFileName:
                    continue
                if file.endswith(".py") and file != '__init__.py':  # 如果是py文件并且不是包的__init__.py
                    if file.startswith('test_'):
                        self.testFile_list.append(os.path.join(root, file))
                    else:
                        self.pageFile_list.append(os.path.join(root, file))
        return self.pageFile_list, self.testFile_list

    def visit_test_files(self):
        """遍历所有test文件，得到所有func"""
        threads = []

        def fun(file_path):
            with open(file_path, 'rb', ) as f:
                root_node = ast.parse(f.read())
            visitor = CodeVisitor()
            parentage = Parentage()
            parentage.visit(root_node)
            visitor.visit(root_node)
            self.tests[file_path.split('test_case\\')[-1]] = visitor.funcNames

        for file_path in self.testFile_list:
            thread = Thread(target=fun, args=(file_path,))
            threads.append(thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # for file_path in self.testFile_list:
        #     fun(file_path)

    def visit_page_files(self):
        """遍历所有page文件，得到所有func"""
        threads = []

        def fun(file_path):
            with open(file_path, 'rb') as f:
                root_node = ast.parse(f.read())
            visitor = CodeVisitor(False)
            parentage = Parentage()
            parentage.visit(root_node)
            visitor.visit(root_node)
            self.pages[file_path.split('test_case\\')[-1]] = visitor.funcNames

        for file_path in self.pageFile_list:
            thread = Thread(target=fun, args=(file_path,))
            threads.append(thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()


class CodeVisitor(ast.NodeTransformer):
    def __init__(self, is_test_case=True):
        self.funcNames = {}
        self.exceptNames = ['setUpClass', 'setUp', 'tearDownClass', 'tearDown', '__init__']
        self.isTestCase = is_test_case

    def visit_FunctionDef(self, node):
        parent_name = node.parent.name if node.parent else '_noCls_'
        if parent_name not in self.funcNames:
            self.funcNames[parent_name] = []
        if self.isTestCase and node.name.startswith('test'):
            self.funcNames[parent_name].append(node.name)
        elif not self.isTestCase:
            self.funcNames[parent_name].append(node.name)
        self.generic_visit(node)


global parent


class Parentage(ast.NodeTransformer):
    parent = None

    def visit(self, node):
        if isinstance(node, ast.ClassDef):
            self.parent = node

        elif isinstance(node, ast.FunctionDef):
            node.parent = self.parent
        node = super().visit(node)

        return node
