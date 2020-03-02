FROM python:latest
RUN apt-get update
COPY MongoDB_Docker /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]