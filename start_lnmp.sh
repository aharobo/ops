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

Echo_Green " Update YUM Repo ... "
yum -y install wget
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo_bak
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum makecache
yum -y update

Echo_Green " Download LNMP Installer ..."

lnmpd=lnmp1.6; lnmp=lnmp1.6.tar.gz
lnmp_url=http://soft.vpser.net/lnmp/lnmp1.6.tar.gz
rm -rf ${lnmp};wget ${lnmp_url} ;tar xvf ${lnmp}
cd ${lnmpd} ; pwd; ls
 
Echo_Green " Adjust LNMP Script ..."
sed -i "s/Install_PHP_/\return;#/g" install.sh
sed -i "s/Install_Libiconv/\#Install_Libiconv/g" install.sh
sed -i "s/Install_Libmcrypt/\#Install_Libmcrypt/g" install.sh
sed -i "s/Install_Mhash/\#Install_Mhash/g" install.sh
sed -i "s/Install_Mcrypt/\#Install_Mcrypt/g" install.sh
sed -i "s/Install_Freetype/\#Install_Freetype/g" install.sh
sed -i "s/Check_PHP_Option/\#Check_PHP_Option/g" install.sh
sed -i "s/Install_PHP/\#Install_PHP/g" install.sh
sed -i "s/LNMP_PHP_Opt/\#LNMP_PHP_Opt/g" install.sh
sed -i "s/Creat_PHP_Tools/\#Creat_PHP_Tools/g" install.sh
sed -i "s/isPHP=\"\"/\isPHP=\"ok\";return;/g" include/end.sh
sed -i "s/Check_PHP_Files/\\#Check_PHP_Files/g" include/end.sh

chmod 775 ./*.sh
sudo ./install.sh



