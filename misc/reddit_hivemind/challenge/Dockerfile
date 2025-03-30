FROM python:3.9-slim


WORKDIR /app

RUN useradd -ms /bin/bash chall

COPY app/requirements.txt .
RUN pip install --ignore-installed -r requirements.txt

COPY app/. .

USER root
RUN chown -R chall /app

USER chall

CMD [ "python3", "app.py"]