#
# Install MySQL 5.5 & Python for tests
#

FROM ubuntu:12.10

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python python-pip

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y wget

#Allow installation of mysqld
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -s /bin/true /sbin/initctl

RUN DEBIAN_FRONTEND=noninteractive apt-get install libaio1

RUN wget http://cdn.mysql.com/Downloads/MySQL-5.6/mysql-5.6.12-debian6.0-x86_64.deb
RUN dpkg -i mysql-5.6.12-debian6.0-x86_64.deb

ADD docker/mysql5.6/my.cnf /etc/my.cnf
RUN mkdir /var/log/mysql/
RUN /opt/mysql/server-5.6/scripts/mysql_install_db --user=root

RUN apt-get clean -y

RUN pip install pymysql

ADD docker/mysql5.6/run.sh /run.sh
ADD . /src

CMD ["/bin/bash", "/run.sh"]
