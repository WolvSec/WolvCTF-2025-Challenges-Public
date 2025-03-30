FROM tensorflow/tensorflow:latest

WORKDIR /app

RUN useradd -ms /bin/bash chall

COPY app/requirements.txt .
RUN pip install --ignore-installed -r requirements.txt

COPY app/. .

USER root
RUN chown -R chall /app
RUN apt-get update \
  && apt-get -y install tesseract-ocr
USER chall

CMD [ "python3", "app.py"]