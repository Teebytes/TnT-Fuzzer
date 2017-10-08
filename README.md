# TnT-Fuzzer
OpenAPI (swagger) fuzzer written in python. This fuzzer is like dynamite for your API!  

## Installation

### Dependencies
TnT-Fuzzer is written in **python 2.7**. All dependencies are listed in requirements.txt and can be installed via pip:

```
pip install -r requirements.txt
```

## Documentation

When run, TnT-Fuzzer logs all responses in a table on commandline: 

| operation | url | response code | response message | response body |
|---|---|---|---|---|
| get       | http://localhost:8080/v2/apicall | 200 | Successful Operation | {'success': true} |
