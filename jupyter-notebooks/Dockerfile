FROM python:3.8.5

EXPOSE 8888

COPY ./requirements.txt .

RUN pip install -r requirements.txt \
  && pip install fbprophet==0.7.1

COPY ./prophet-notebooks /prophet-notebooks
COPY ./data /data

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--notebook-dir", "/prophet-notebooks"]
