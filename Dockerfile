FROM python:3.11.3

WORKDIR /app

COPY requirements.txt .

RUN  pip install --no-cache-dir -r requirements.txt

COPY . .


ENV DATABASE_URI='mysql+mysqlconnector://root:@mysql-db:3306/db-related-entities'

CMD ["python", "main.py"]
