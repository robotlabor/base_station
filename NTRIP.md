# Mobile Base station custom NTRIP server configuration

## 1. Aim

The aim of this subproject is to create a custom NTRIP server for the GNSS-RTK base station for the Traffic Cone Manipulator mobile robot platform.

## 2. Hardware setup

Our mobile base station consists of the following components:

- Raspberry Pi 4
- Sirius RTK GNSS - F9P
- RTK F9P GNSS antenna
- Battery and power management system

## 3. System information and dependencies

- Operating system: Ubuntu 20.04
- Applied Python package: <a href="https://github.com/semuconsulting/pygnssutils"><i>pygnssutils</i></a>

## 4. Installation

- Check the USB port used by the Sirius RTK GNSS: 

```ls/dev/tty*```

- Install <a href="https://github.com/semuconsulting/pygnssutils"><i>pygnssutils</i></a>:

```python3 -m pip install --upgrade pygnssutils```

- Install <i>openvpn</i>:

```sudo openvpn -config <vpn-file>```

## 5. Usage

- Start NTRIP client:

```gnssntripclient -S hostip -P 2101 -M pygnssutils --user anon --password password```

- Start the <i>base_startup</i> shell script. This can be added to <i>crontab</i> for automatic startup.

- Default NTRIP login credentials, which can be changed in the <i>pygnssutils</i> launch file:
    - Mountpoint: <i>pygnssutils</i>
    - Username: <i>anon</i>
    - Password: <i>password</i>

## 6. Packages used for NTRIP monitoring

- <i>serial</i>
- <i>pyubx2</i>
- <i>time</i>
- <i>lgpio</i>

## 7. Other useful information for development

- Pygnssutils package install location: <i>home/base/.local/lib/python3.10/site-packages/pygnssutils</i>
- Other useful information about the pygnssutils package: <a href="https://www.semuconsulting.com/pygnssutils/py-modindex.html"><i>more information</i></a>
<br />
<br />

|   |   | 
|:-:|:-:|
|![ARNLlogo](ARNL.png)|![JKKlogo](image-2.png)|




