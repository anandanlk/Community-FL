FROM python:3.12.4-slim

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8088"]