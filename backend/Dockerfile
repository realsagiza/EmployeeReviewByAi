# Dockerfile สำหรับ backend
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโฟลเดอร์ app ทั้งหมดไปยัง /app
COPY ./app /app

CMD ["python", "main.py"]
