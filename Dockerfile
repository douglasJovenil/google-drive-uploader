FROM python:3-alpine3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pipenv pipfile-requirements && \
    pipfile2req > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt -U --target /app/site-packages && \
    pip uninstall pipenv pipfile-requirements -y && \
    rm Pipfile Pipfile.lock requirements.txt

ENV PYTHONPATH /app/site-packages

CMD python src/main.py
