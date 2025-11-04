import sys
import os

# 添加项目根目录到 Python 路径（支持直接运行）
# 获取当前文件的目录（be/）
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（be/ 的父目录）
project_root = os.path.dirname(current_dir)
# 添加到 Python 路径（如果不在路径中）
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from be import serve

if __name__ == "__main__":
    serve.be_run()
