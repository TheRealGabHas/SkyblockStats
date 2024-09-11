FROM python:3.12-alpine

WORKDIR /app

COPY src .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3.12", "-m", "uvicorn", "main:app", "--no-server-header", "--host", "0.0.0.0"]