FROM python:3.7

WORKDIR /belvo-transactions

COPY requirements.txt /belvo-transactions
RUN pip install -r /belvo-transactions/requirements.txt

COPY run.py /belvo-transactions
ADD . /belvo-transactions

EXPOSE 5000
CMD ["python", "/belvo-transactions/run.py"]
