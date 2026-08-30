FROM python
WORKDIR /home/myapp
COPY ./database.py /home/myapp/
COPY ./producer.py /home/myapp/
COPY ./scheduler.py /home/myapp/
COPY ./requirements.txt /home/myapp/
RUN pip install -r /home/myapp/requirements.txt
CMD ["python", "-u", "/home/myapp/scheduler.py"]
