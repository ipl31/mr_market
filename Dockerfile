FROM python:3.8-slim
WORKDIR /mr_market
COPY . /mr_market/
RUN python setup.py install
CMD ["mister_market"]
