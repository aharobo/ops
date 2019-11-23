#!/bin/bash
array=($(ls /etc/sysconfig/network-scripts))
path=/etc/sysconfig/network-scripts/
name=ifcfg-eth0
file="`echo ${array[*]} | grep -o 'ifcfg-ens[[:digit:]]\+'`"

judge() {
  if [ -f $path$file ]; then
    echo "the net name is not modified"
  else
    echo "$path$file was modified"
    exit
  fi
}

DM() {
  if [ `grep -o 'DEVICE' $path$file | wc -l` -eq 1 ]; then
    sed -i 's/DEVICE=.*/DEVICE="eth0"/' $path$file &>/dev/null
  fi
}

NM() {
  if [ `grep -o 'NAME' $path$file | wc -l` -eq 1 ]; then
    sed -i 's/NAME=.*/NAME="eth0"/' $path$file
  fi
}

other() {
  mv $path$file $path$name
  if [ -f "/etc/default/grub" ]; then
    sed -i '/^GRUB_CMDLINE_LINUX/c \GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root "net.ifnames=0 biosdevname=0" rd.lvm.lv=centos/swap rhgb quiet"' /etc/default/grub 
    grub2-mkconfig -o /boot/grub2/grub.cfg &>/tmp/1.txt
    if [ `grep 'done' /tmp/1.txt | wc -l` -eq 1 ]; then
      echo "禁止可预测命名规则成功。"
    else
      echo "禁止可预测命名规则失败。"
    fi
    cat /dev/null >/tmp/1.txt
  fi
}

read -p "Do you want to modify the net name: {yes|no} " choice
case $choice in
  yes)
    judge
    sleep 1
    DM
    sleep 1
    NM
    sleep 1
    other
    sleep 3
    echo "$name was modified,please restart your linux" ;;
  no)
    echo "you will quit."
    sleep 3 ;;
  *)
    echo "Please input {yes|no}"
esac
