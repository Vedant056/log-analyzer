FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY Log_Analyzer.py .
COPY sample_auth.log .

EXPOSE 5000

CMD ["python", "app.py"]