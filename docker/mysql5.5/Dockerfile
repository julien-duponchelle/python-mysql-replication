#
# Install MySQL 5.5 & Python for tests
#

FROM ubuntu:12.10

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-pip

#Allow installation of mysqld
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server-5.5
ADD docker/mysql5.5/mysqld_replication.cnf /etc/mysql/conf.d/mysqld_replication.cnf 

RUN apt-get clean -y

RUN DEBIAN_FRONTEND=noninteractive pip install pymysql

ADD docker/mysql5.5/run.sh /run.sh
ADD . /src

CMD ["/bin/bash", "/run.sh"]
