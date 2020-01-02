FROM python:3.8-alpine

RUN adduser -D bjml

WORKDIR /home/bjml

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R bjml:bjml ./
USER bjml

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]
