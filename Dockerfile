FROM python:3.8-slim
WORKDIR /mr_market
COPY . /mr_market/
RUN apt-get install -y build-essential python-dev && python setup.py install
CMD ["mister_market"]
