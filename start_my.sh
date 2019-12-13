#!/bin/bash
clear

python3 /var/ops/ip_up_push.py auto true auto_pi_rc_login

temp=$(cat /sys/class/thermal/thermal_zone0/temp); 

echo Current CPU TEMP:${temp: 0:-3}C

echo "HELLO BOY"
