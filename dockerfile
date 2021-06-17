FROM ubuntu:18.04
RUN apt-get -y update
RUN apt-get -y install git wget autoconf automake libtool curl make g++ unzip cmake python3 python3-dev python3-sip-dev

RUN wget https://github.com/google/protobuf/releases/download/v3.5.0/protobuf-all-3.5.0.zip

RUN git clone https://github.com/Ultimaker/libArcus.git
RUN git clone https://github.com/JRyanShue/ZengerCuraEngine.git

# install protobuf
RUN unzip protobuf-all-3.5.0.zip
WORKDIR "/protobuf-3.5.0"
RUN ./autogen.sh && ./configure && make && make install && ldconfig

# install libArcus
WORKDIR "/libArcus"
RUN git pull
RUN git checkout 4.4
RUN mkdir build && cd build && cmake .. && make && make install

# install curaengine
WORKDIR "/ZengerCuraEngine"
RUN git pull
RUN git checkout 4.4
RUN mkdir build && cd build && cmake .. && make

# C++ portion installation done
# insert python and other scripts within the same working directory, install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY resources/ .
COPY static/ .
COPY templates/ .

# Specify the command to run on container start
CMD [ "python", "./app.py" ]

# Set base image (host OS) <- this used to be at the beginning of the python stuff
# FROM python:3.8-alpine

# By default, listen on port 5000 <- used to be right after setting base image
# EXPOSE 5000/tcp
