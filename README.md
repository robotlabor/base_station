# Mobile Base Station for Traffic Cone Manipulator Robot

## 1. Aim

The aim of subproject is to create a custom GNSS-RTK base station for the Traffic Cone Manipulator mobile robot platform. The base station consists of off-the-shelf components, but the custom-built hardware and software system allows us to develop solutions in accordance with the project's custom requirements. 

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

```sudo openvpn-config <vpn-file>```

## 5. Usage

- Start NTRIP client:

```gnssntripclient -S hostip -P 2101 -M pygnssutils --user anon --password password```

- Start the <i>base_startup</i> shell script. This can be added to <i>crontab</i> for automatic startup. 

<br />
<br />






