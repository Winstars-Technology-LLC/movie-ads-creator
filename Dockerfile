FROM python:3.7

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]