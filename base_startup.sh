#!/bin/bash
sleep 50
#rendszergazda jog adása a portnak
sudo chmod a+rw /dev/ttyACM0
#vpn csatlakozás
sudo openvpn --config /home/base/Desktop/vpnkey/test2.ovpn > /dev/null 2>&1 &
sleep 5
#ntrip server indítása
#sudo gnssserver --inport "/dev/ttyACM0" --hostip 10.11.0.26 --outport 2101 --ntripmode 1 --protfilter 4 --format 2 &
#sudo gnssserver --inport "/dev/ttyACM0" --hostip 192.168.2.128 --outport 2101 --ntripmode 1 --protfilter 4 --format 2 &
sudo gnssserver --inport "/dev/ttyACM0" --hostip 172.20.10.13 --outport 2101 --ntripmode 1 --protfilter 4 --format 2 > ~/Desktop/gnssserver_output.txt 2>&1 &
sleep 10
#survey-in állapot olvasása
sudo python3 /home/base/Desktop/read_survey_in_status.py &
