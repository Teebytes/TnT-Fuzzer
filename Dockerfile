FROM python:3.11.0a5-alpine3.15

WORKDIR /app

COPY requirements.txt .

RUN apk add git --update 
RUN git clone https://github.com/mseclab/PyJFuzz.git && cd PyJFuzz && python setup.py install
RUN rm -rf PyJFuzz
RUN cd ..
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "tntfuzzer/tntfuzzer.py"]