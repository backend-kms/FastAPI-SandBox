import os

from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
HASH_ALGORITHM = os.environ["HASH_ALGORITHM"]
SECRET_KEY = os.environ["SECRET_KEY"]
