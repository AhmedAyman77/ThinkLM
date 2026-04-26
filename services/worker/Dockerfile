FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python -c "import tiktoken; tiktoken.get_encoding('cl100k_base')"

COPY . .

CMD ["python", "main.py"]