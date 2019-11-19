#!/bin/bash

echo -e "\033[31m \033[05m Backup Gogs \033[0m"

current=`date "+%Y-%m-%d %H:%M:%S"`  
timeStamp=`date -d "$current" +%s`   
currentTimeStamp=$((timeStamp*1000+`date "+%N"`/1000000)) 
gogs_sql_name="gogs_sql_${currentTimeStamp}.sql"
gogs_app_name="gogs_app_${currentTimeStamp}.zip"
gogs_repo_name="gogs_repo_${currentTimeStamp}.zip"

gogs_app_src="/home/gogs"
gogs_repo_src="/home/git/"

echo -e "\033[31m \033[05m Source Intsall Path : gogs_app_src =${gogs_app_src},gogs_repo_src=${gogs_repo_src} \033[0m"

echo -e "\033[41;36m Backup Database gogs \033[0m"
read -p "Press any key to start" var  
mysqldump -uFf -pFf2020 gogs > ./${gogs_sql_name}

echo -e "\033[41;36m Backup DATA : ${gogs_repo_src}  \033[0m"
read -p "Press any key to start" var  
zip -r -9  ./${gogs_repo_name} ${gogs_repo_src} 


echo -e "\033[41;36m Backup APP : ${gogs_app_src} \033[0m"
read -p "Press any key to start" var  
zip -r -9  ./${gogs_app_name} ${gogs_app_src} 

 
echo -e "\033[32m  ALL DONE \033[0m" 

ls -l -h

echo -e "\033[32m  By Joe \033[0m" 
