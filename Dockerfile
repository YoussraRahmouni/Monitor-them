FROM ubuntu
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install pylint
RUN apt-get -y install git
RUN apt-get -y install musl-dev
RUN apt-get install libffi-dev
RUN apt-get install openssl
RUN apt-get -y install python3-pip
RUN pip install paramiko
RUN pip install apache-log-parser
RUN pip install coverage
RUN pip install dash
RUN pip install pandas
COPY ./ /projet
ENTRYPOINT ["python3", "/projet/interface.py"]
