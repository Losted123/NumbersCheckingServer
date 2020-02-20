FROM python:latest
RUN apt-get update
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]