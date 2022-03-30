Raspberry Pi Introduction
=========================

Welcome! The Raspberry Pi (RPi) is a great tool to empower your creativity. Discover the multiple possibilities this single board computer brings to you.

Table of contents
-----------------
- [Table of contents](#table-of-contents)
- [Compare boards](#compare-boards)
- [Terminology](#terminology)
- [Pin-out](#pin-out)
  * [Friendly orientation](#friendly-orientation)
  * [Interactive guide](#interactive-guide)
  * [Other considerations](#other-considerations)
- [Setup](#setup)
  * [Requirements](#requirements)
  * [Installation Steps](#installation-steps)
  * [Login instructions](#login-instructions)
  * [Wi-Fi instructions](#wi-fi-instructions)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

Compare boards
--------------

The following table could be used as a quick comparison between two versions of the RPi

| Raspberry Pi 3 Model B   | Raspberry Pi 4 Model B   |
|--------------------------|--------------------------|
| Broadcom [BCM2837][1]    | Broadcom [BCM2711][2]    |
| Quad-Core 64bit @ 1.2GHz | Quad-core 64bit @ 1.5GHz |
| [Cortex A53][3] (ARM v8) | [Cortex A72][4] (ARM v8) |
| 1GB LPDDR2 SDRAM         | 2GB, 4GB or 8GB LPDDR4   |
| 100 Base Ethernet        | Gigabit Ethernet         |
| [Official page][5]       | [Official page][6]       |

Terminology
-----------
* RPi: Raspberry Pi is a series of small single-board computers (SBCs) developed in the United Kingdom by 
the Raspberry Pi Foundation in association with Broadcom. [[source]][7]
* SBC: Single board computer is a complete computer built on a single circuit board, with microprocessor(s), memory, 
input/output (I/O) and other features required of a functional computer. [[source]][8]


Pin-out
-------
A great advantage about RPi is that you can interact with the hardware. Also consider using a hat for this purpose.

### Friendly orientation 

The image is of the RPi 3, but it applies for the RPi 4. More details *https://medium.com/youngwonks/raspberry-pi-3-pinout-50b904ed41f0*

![Pin-out](https://miro.medium.com/max/1400/1*A2gpUDLyOx903dVUStHFTA.jpeg)

### Interactive guide

More details *https://pinout.xyz/*

![Pin-out](https://raw.githubusercontent.com/Gadgetoid/Pinout.xyz/master/resources/raspberry-pi-pinout.png)

```shell
# https://gpiozero.readthedocs.io/en/stable/installing.html
sudo apt update
sudo apt install python3-gpiozero
pinout
```

### Other considerations

Take note of the white pins. More details *https://projects.raspberrypi.org/en/projects/physical-computing/1*

![Advanced usage](https://projects-static.raspberrypi.org/projects/physical-computing/765b944f3fe3d57bd3568794ff6527f72b57ddc8/en/images/pinout.png)

For older [versions][9]

Setup
-----

### Requirements

Basic elements
- Raspberry Pi 3 Model B
- SD card 32GB
- Power cable 2.5A MicroUSB

There are two options, please make sure to at least have one of the following options
1. External monitor option
   1. HDMI monitor
   2. HDMI cable
   3. USB keyboard
2. Ethernet cable option
   1. Ethernet Cable
   2. A computer with RJ45 port


### Installation Steps
1. [Download Raspberry Pi Imager][10]

![Download windows](https://raspberrytec.blob.core.windows.net/images/download-windows.png)

2. Install the application. Use default options
3. Open Raspberry Pi Imager
4. Choose **Raspberry Pi OS (other) > Raspberry Pi OS Lite(64-bit)**

![pi os](https://raspberrytec.blob.core.windows.net/images/pios-lite.png)

5. Select your SD as storage

![Storage](https://raspberrytec.blob.core.windows.net/images/chose-storage.png)

6. Click on Gear Icon ⚙️
7. Use the following values

- [ ] Disable overscan
- [ ] Set hostname
- [x] Enable SSH
  - [x] Use password authentication
  - [ ] Allow public-key authentication only
- [x] Set username and password
  - Username: pi
  - Password: raspberry
- [ ] Configure wifi
- [ ] Set locale settings
- [ ] Play sound when finished
- [x] Eject media when finished
- [x] Enable telemetry

9. Click on **WRITE > YES**

### Login instructions

> Get the ip of the raspberry from the powershell `ping raspberrypi.local -4`

1. Connect the external devices
   1. Option A: Connect a keyboard, power and monitor
   2. Option B: Connect ethernet to your computer and power
      1. Open a powershell
      2. Install 64-but x86 [PuTTY][11] with default options
      3. Open PuTTY
      4. Set Host Name `raspberrypi.local`
      5. Connection type [ssh][12]
      6. Click on **Save** and then **Open**
      7. Click on **Accept** in the Security Alert
2. Set credentials
   1. raspberrypi login (login as): pi
   2. Password: raspberry
3. Optional, turn off the RPi `shutdown now`

> You can also connect via `ssh pi@raspberrypi.local`

### Wi-Fi instructions

References, [[14]][14], [[15]][15]

1. Set country code [ISO 3166-1][13] 
```shell
sudo raspi-config nonint do_wifi_country MX
```

2. Open the _wpa_supplicant.conf_

````shell
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
````

3. Add network configuration

Wireless network `wpa_passphrase "network_name"`
```shell
network={
  ssid="network_name"
  scan_ssid=1
  psk=e647e6a0df46537ad98c7687fa75fa33f0e0489f80fec9ed0180058647724073
}
```
 PEAP network `echo -n "plaintext_password" | iconv -t utf16le | openssl md4`
```shell
network={
  ssid="<<network_name>>"
  priority=1
  proto=RSN
  key_mgmt=WPA-EAP
  pairwise=CCMP
  auth_alg=OPEN
  eap=PEAP
  identity="<<user_name>>"
  password=hash:<<the_hash>>
  phase1="peaplabel=0"
  phase2="auth=MSCHAPV2"
}
 ```
4. Apply changes
````shell
sudo reboot
````

Switch a LED
------------

1. Open a python shell
````shell
python
````
2. Declare LED
````python
from gpiozero import LED
led = LED(14)
````
3. Turn on LED
````python
led.on()
````
4. Turn off LED
````python
led.off()
````
5. Exit
````python
exit()
````

VSCode setup
------------
1. Download [VS Code](https://code.visualstudio.com/docs/?dv=win)
2. Install [Remote SSH Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
3. Add ssh project
4. Open workspace folder 
5. Run python scripts as `python blink_simple.py`

Other resources
---------------
https://github.com/raspberrypilearning/physical-computing-guide/blob/master/pull_up_down.md
https://gpiozero.readthedocs.io/en/stable/

[//]: # (References)
[1]: https://www.raspberrypi.com/documentation/computers/processors.html#bcm2837
[2]: https://www.raspberrypi.com/documentation/computers/processors.html#bcm2711
[3]: https://developer.arm.com/Processors/Cortex-A53
[4]: https://developer.arm.com/Processors/Cortex-A72
[5]: https://www.raspberrypi.com/products/raspberry-pi-3-model-b/
[6]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[7]: https://en.wikipedia.org/wiki/Raspberry_Pi
[8]: https://en.wikipedia.org/wiki/Single-board_computer
[9]: https://files.pimylifeup.com/gpiopinout/Raspberry%20Pi%20GPIO%20Pinout%20Key%20-%20PiMyLifeUp.pdf
[10]: https://www.raspberrypi.com/software/
[11]: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
[12]: https://www.ssh.com/academy/ssh/protocol
[13]: https://en.wikipedia.org/wiki/ISO_3166-1
[14]: https://blog.iamlevi.net/2017/01/connect-raspberry-pi-peap-mschap-v2-wifi/
[15]: https://raspberrytips.com/raspberry-pi-wifi-setup/
