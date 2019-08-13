#!/bin/bash

Echo_Red()
{ 
	echo $(Color_Text "$1" "31")
}
Echo_Green()
{
	echo $(Color_Text "$1" "32")
}
Echo_Yellow()
{
	echo -n $(Color_Text "$1" "33")
}

PythonUrl=https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
PythonUrl=http://39.100.226.226/Python-3.6.1.tgz
PythonZip=Python-3.6.1
WebRoot=/home/wwwroot/

Echo_Green " █ Install libs & Download... "

yum -y install  build-essential psmisc python-dev libxml2 libxml2-dev epel-release
yum -y install  python-pip
pip install --upgrade pip
yum install sqlite*
yum install -y openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel   gcc


wget ${PythonUrl}
tar xvf ${PythonZip}.tgz

Echo_Green " Install Python ... "
cd  ${PythonZip} ;pwd; ls
./configure --prefix=/usr/local/python
make && make install


mv /usr/bin/python /usr/bin/python.bak
mv /usr/bin/pip /usr/bin/pip.bak
#重命名python2的快捷方式

ln -s /usr/local/python/bin/python3 /usr/bin/python
ln -s /usr/local/python/bin/pip3 /usr/bin/pip
#创建python3与pip3软连接

Echo_Green " █ Adjust Python2 Script ..."
ll /usr/bin/yum*
sed -i "s/python/\python2/g"  /usr/bin/yum
sed -i "s/python/\python2/g"  /usr/libexec/urlgrabber-ext-down
cd
echo 'export PATH=$PATH:/usr/local/python/bin/' >> /etc/profile
source /etc/profile

Echo_Green " █ Install Django  ..."

yum install -y python-devel python-setuptools -y mysql-devel  MySQL-python
pip install django==2.1.8 
sudo find /usr -name django-admin
ln -s /usr/local/python/bin/django-admin /usr/bin/django-admin

Echo_Green " █ Install Django  Test Project ..."

DJ_PROJECT_NAME=pyweb

cd ${WebRoot}
django-admin startproject ${DJ_PROJECT_NAME}
cd pyweb/
python manage.py startapp app

Echo_Green " █ Install gunicorn ..."

pip install gunicorn 

echo 'gunicorn pyweb.wsgi:application -b 0.0.0.0:8000 -w 4 -k gthread '
echo 'gunicorn pyweb.wsgi:application'
echo 'gunicorn --config=config.py pyweb.wsgi:application'
echo 'nohup  gunicorn --config=config.py pyweb.wsgi:application >/dev/null 2>&1 &'
echo "ps -ef |grep gunicorn|grep -v grep|awk '{print $2}'| xargs kill -9"
ls

Echo_Green " █ start gunicorn ..."

cat > ./config.py <<EOF

import multiprocessing 
bind = "0.0.0.0:8000"
workers =multiprocessing.cpu_count() * 2 + 1

EOF
chmod 777 ./config.py
nohup  gunicorn --config=config.py pyweb.wsgi:application >/dev/null 2>&1 &

 

cat > ./kill <<EOF

sudo nohup gunicorn ${DJ_PROJECT_NAME}.wsgi:application -b 0.0.0.0:8000&

#也可以直接启动
gunicorn ${DJ_PROJECT_NAME}.wsgi:application -b 0.0.0.0:8000 -w 4 -k gthread

gunicorn pyweb.wsgi:application -b 0.0.0.0:8000 -w 4 -k gthread

gunicorn manage:app -c gunicorn.conf.py
pstree -ap|grep gunicorn

gunicorn pyweb.wsgi:application -b 0.0.0.0:8000 -w 4 -k gthread
gunicorn pyweb.wsgi:application
gunicorn --config=config.py pyweb.wsgi:application
nohup  gunicorn --config=config.py pyweb.wsgi:application >/dev/null 2>&1 &
ps -ef |grep gunicorn|grep -v grep|awk '{print $2}'| xargs kill -9


gunicorn -c gunicorn.conf.py ${DJ_PROJECT_NAME}.wsgi:application

#以gunicorn.conf.py配置文件启动gunicorn
gunicorn -c gunicorn.conf.py api.wsgi:application


杀死gunicorn进程

ps -ef |grep gunicorn|grep -v grep|awk '{print $2}'| xargs kill -9

#也可以直接启动
gunicorn ${DJ_PROJECT_NAME}.wsgi:application -b 0.0.0.0:8000 -w 4 -k gthread

#gunicorn ${DJ_PROJECT_NAME}.wsgi:application -b 0.0.0.0:8091 -w 4 -k gthread  --thread 40 --max-requests 4096 --max-requests-jitter 512

sudo pkill -f uwsgi -9

uwsgi  --ini  uwsgi.ini

uwsgi --stop uwsgi.pid

uwsgi --reload uwsgi.pid

uwsgi --http 0.0.0.0:8000 --file ${DJ_PROJECT_NAME}/wsgi.py --static-map=/static=static


pip freeze > pkg.txt
将当前生产环境下 Python 的模块收集起来存放到 pkg.txt 文件里
pip install -r pkg.txt
在部署环境下降生产环境下的需要模块全部安装

EOF
chmod 777 ./kill; cat ./kill


 



