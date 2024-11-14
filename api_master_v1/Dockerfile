FROM ubuntu:22.04

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN apt-get update

RUN apt-get -y install gunicorn 

RUN apt-get -y install libzbar0

RUN apt-get install -y python3-pip 

RUN apt-get install -y libgl1
# RUN apt-get install libmysqlclient-dev

RUN pip3 install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 5009

# run the command
# CMD ["uvicorn", "api:service_api", "--host","0.0.0.0", "--port",  "5009"]

CMD ["gunicorn", "--bind", "0.0.0.0:5009", "server:platform_api"]