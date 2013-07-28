echo "Start mysql daemon"
mysqld --user=root &
echo "Wait for mysql daemon"
STATUS=1
while [ $STATUS -ne 0 ]
do
  echo "SHOW DATABASES" | mysql
  STATUS=$?
done
cd /src
python setup.py test
