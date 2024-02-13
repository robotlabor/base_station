Mobil Bázisállomás Dokumentáció
Hardver:

Raspberry Pi 4
RPI PowerPack V1.2
Sirius RTK GNSS Rover (F9P)
RTK F9P GPS Antenna
Információk:

Operációs rendszer: Ubuntu 20.04
Használt Python csomag: https://github.com/semuconsulting/pygnssutils: https://github.com/semuconsulting/pygnssutils
Csomag telepítési helye: home/base/.local/lib/python3.10/site-packages/pygnssutils
Egyéb hasznos információk: https://www.semuconsulting.com/pygnssutils/py-modindex.html: https://www.semuconsulting.com/pygnssutils/py-modindex.html
Használt parancsok:

A vevő portjának megtekintése: ls /dev/tty*
Pygnssutils telepítése: python3 -m pip install --upgrade pygnssutils
NTRIP szerver indítása CLI-ből: gnssserver --inport "/dev/ttyACM0" --hostip 192.168.1.142 --outport 2101 --ntripmode 1 --protfilter 4 --format 2
NTRIP kliens indítása (automatikus csatlakozás mount pointhoz): gnssntripclient -S hostip -P 2101 -M pygnssutils --user anon --password password
Alapértelmezett beállítások mountpointhoz való csatlakozáshoz:
user=anon
password=password
mountpoint=pygnssutils
OpenVPN telepítése: sudo apt-get install openvpn
VPN-re való csatlakozás: sudo openvpn –config *vpn-file neve*
A sudo jelszó elkerülése:
sudo visudo
Utolsó sornak hozzáadni: <username> ALL=(ALL) NOPASSWD: ALL (pl.: dani ALL=(ALL) NOPASSWD: ALL)
A shell script automatikus indítása a rendszer indulásakor:
crontab -e
A fájlhoz hozzáadni: @reboot /path/to/your/base_startup.sh
base_startup.sh tartalma:

Bash
#!/bin/bash
sleep 50
# Port jogosultságainak beállítása
sudo chmod a+rw /dev/ttyACM0
# VPN csatlakozás
sudo openvpn --config /home/base/Desktop/vpnkey/test2.ovpn > /dev/null 2>&1 &
sleep 5
# NTRIP szerver indítása
sudo gnssserver --inport "/dev/ttyACM0" --hostip 172.20.10.13 --outport 2101 --ntripmode 1 --protfilter 4 --format 2 > ~/Desktop/gnssserver_output.txt 2>&1 &
sleep 10
# SURVEY-IN állapot olvasása
sudo python3 /home/base/Desktop/read_survey_in_status.py &
Körültekintően használja a kódot.
read_survey_in_status.py tartalma:

Python
import time
import lgpio
from serial import Serial
from pyubx2 import UBXReader

SURVEY_DURATION = 60
LED_PIROS = 12
LED_ZOLD = 13

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, LED_PIROS)
lgpio.gpio_claim_output(h, LED_ZOLD)

stream = Serial('/dev/ttyACM0', 38400, timeout=5)
ubr = UBXReader(stream)
for raw, parsed in ubr:
    if parsed.identity == "NAV-SVIN":
        print(f"SVIN duration {parsed.dur} ({parsed.dur * 100/SURVEY_DURATION}%), valid? {parsed.valid}, active? {parsed.active}")
        if parsed.valid == 1:
            try:
                while True:
                    lgpio.gpio_write(h, LED_ZOLD
