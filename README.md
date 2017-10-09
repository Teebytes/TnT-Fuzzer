
![](docs/images/logo.jpg)
============
OpenAPI (swagger) fuzzer written in python. This fuzzer is like dynamite for your API!

TnT-Fuzzer is designed to make fuzzing, robustness testing and validation of REST APIs easy and maintainable. After a 
fuzzing run, the log files state the exact history of requests to reenact a crash or misuse. TnT-Fuzzer can be used 
for penetration testing or continued testing of a service in development.  

## Installation
TnT-Fuzzer is written in **python 2.7**

### Dependencies
All dependencies are listed in requirements.txt and can be installed via pip:

```
pip install -r requirements.txt
```

## Documentation

When run, TnT-Fuzzer logs all responses in a table on commandline: 

| operation | url | response code | response message | response body |
|---|---|---|---|---|
| get       | http://localhost:8080/v2/apicall | 200 | Successful Operation | {'success': true} |

### Testing

For testing or development, have a look at the [swagger petstore example](http://petstore.swagger.io/). A local stub 
server can easily be generated and run locally. 
 