FROM python:3.11-slim-bullseye

LABEL MAINTAINER="BlackOrder <4302157+BlackOrder@users.noreply.github.com>"

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN groupadd -r jasmin && useradd -r -g jasmin jasmin

# Install requirements
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get full-upgrade -y
RUN apt-get autoremove -y

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# copy the source code
WORKDIR /build
COPY . .

# install the package
RUN pip install .

# run the package
CMD ["jasminmongologd"]
