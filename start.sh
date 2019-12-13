#!/bin/bash
clear

alias rc='sudo raspi-config'
alias cpu='temp=$(cat /sys/class/thermal/thermal_zone0/temp); echo "Current CPU TEMP:${temp: 0:-3} C$
alias lh='ls -l -h'


sleep  3
cpu
python3 /var/ops/ip_up_push.py auto true aoto_login


echo "HELLO BOY"
