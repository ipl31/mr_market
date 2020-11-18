FROM python:3.8-slim
WORKDIR /mr_market
COPY requirements.txt /mr_market/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /mr_market/
ENTRYPOINT ["python"]
CMD ["/mr_market/main.py"]
