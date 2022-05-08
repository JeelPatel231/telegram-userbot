# ready base for dev env
FROM python:alpine AS base 

RUN mkdir /workdir
WORKDIR /workdir

COPY requirements.txt .
RUN pip3 install -r requirements.txt
CMD [ "/bin/sh" ]

# make the production docker image when needed
FROM base AS deploy
COPY . .
CMD ["python3","main.py"]