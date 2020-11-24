## A twitter bot that automates answering FAQs from INEC 

## Setup
These steps helps to configure your development environment.

- create a virtual environment  to isolate your development environment.
```shell script
    $ python -m venv <devenv>   
```
- activate virtual environment.
```shell script
    $ source <venv>/bin/activate
```
- clone git repo 
```shell script
    $ git clone git@github.com:beesaferoot/weenec.git
```
- cd to project directory
```shell script
    $ cd weenec
```
- install requirements
```shell script
    $ pip install -r requirements.txt
```
- export twitter credentials 
```shell script
    $ export CONSUMER_KEY=<API_KEY>
    $ export CONSUMER_SECRET=<API_SECRET_KEY>
    $ export ACCESS_TOKEN=<ACCESS_KEY>
    $ export ACCESS_TOKEN_SECRET=<ACCESS_SECRET_KEY>
```

## Setup Message Queue
Steps to install and configure RabbitMQ using docker.
- enquire you have docker installed. visit [docker installation guide.](https://docs.docker.com/get-docker/)
- run docker command
```shell script
    $ docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
## Requirements
- tweepy==3.9.0
- chatterbot==1.0.8
- pika==1.1.0
- rabbitmq
- docker

## Runtime
- Python3.6
