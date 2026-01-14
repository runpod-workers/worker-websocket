FROM python:3.12-slim

WORKDIR /
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY handler.py /

CMD ["python3", "-u", "handler.py"]
