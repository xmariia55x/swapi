FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mv .env.template .env

EXPOSE 5000

CMD ["python", "main.py"]
