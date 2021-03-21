FROM python:3.9-alpine

WORKDIR /mnt
ENV FLASK_APP=/mnt/app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt /mnt
RUN pip install -r requirements.txt

COPY . /mnt/

EXPOSE 5000
CMD ["flask", "run"]
