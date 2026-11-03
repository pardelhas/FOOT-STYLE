FROM python:3.12

RUN pip install flask

COPY main.py /main.py

COPY templates /templates

EXPOSE 5000

CMD ["python", "/main.py"]