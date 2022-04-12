FROM python:alpine

RUN mkdir /workdir
WORKDIR /workdir

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3","main.py"]