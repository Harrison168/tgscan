import os
from dotenv import load_dotenv
from pathlib import Path

# 获取当前文件的目录
current_dir = Path(__file__).resolve().parent

# 获取项目根目录（假设 common.py 在 src/utils 目录下）
root_dir = current_dir.parent.parent

# 根据环境变量选择加载的 .env 文件
# 环境参数：dev,prod
ENV = os.getenv('ENVIRONMENT', 'prod')
dotenv_path = root_dir / f".env.{ENV}"

# 加载对应的 .env 文件
load_dotenv(dotenv_path)

# 获取环境变量
DEBUG_MODE = os.getenv('DEBUG_MODE')
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

print(f"Current environment: {ENV}")
