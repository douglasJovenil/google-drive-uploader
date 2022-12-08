FROM python:3.10

WORKDIR /app

COPY . .

RUN apt-get update -y
RUN pip install pipenv pipfile-requirements
RUN pipfile2req > requirements.txt
RUN pip install -r requirements.txt

CMD python src/main.py
