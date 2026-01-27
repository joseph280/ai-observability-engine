#1. Base Image: start with a lightweight Python Linux setup
FROM python:3.13-slim

#2. Setup Env
ENV PYTHONUNBUFFERED=1

#3. Work Directory
WORKDIR /app

#4. Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#5. Application
COPY . .

#6. Run
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]

