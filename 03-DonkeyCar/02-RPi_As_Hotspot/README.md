# Wireless Donkey Car

Instructions for how to setup RPi 3B for DonkeyCar as own hotspot -- The motivation for this change to the
[Donkey Car](https://github.com/autorope/donkeycar/) project is to use the Raspberry Pi 3's built-in Wi-Fi
to connect to the car to control it.

## A Donkey 2.5.8 Based Image

A [Donkey release 2.5.8](https://github.com/autorope/donkeycar/releases) based
[image](https://drive.google.com/open?id=1PilLO1pO8E0svKNTesbsRzfwsOkGkmfx) (⇐ Click to download from Google Drive)
is created to accelerate deployment.

The image is downloaded as a 1.3GB .zip compressed file. It unzips into a 3GB .img file, with a file name that says 2.5.0
-- Ignore that discrepency for now, it will be fixed later. The .img file may be used to burn a 32GB SD card using any
SD writing tool, such as [etcher](https://www.balena.io/etcher/).

## Connecting to the Car with Wi-Fi

Once the RPi3 on the car is started, a new Wi-Fi access point should show up on any 802.11b/g/n device,
with the SSID ```LXLCar```. (If you don't see that, the RPi3's ethernet port may be used for troubleshooting.)

The Wi-Fi key is ```A2AutonomousVehicle```. After connecting on that Wi-Fi connection, say with a laptop,
the laptop should get an IP address in the range of ```192.168.89.xxx```. The car's IP address is ```192.168.89.1```.

## SSH into the Car

I used openssh, and here is my configuration for connecting to the car in ```~/.ssh/config```:
```
Host  mycar
      Hostname 192.168.89.1
      Identity ~/.ssh/id_mycar
      User pi
```
The user ```pi```'s password is ```RaspberryPi```.

Here is the private key (This private SSH key is not encrypted. So DO NOT use it for
anything else but the donkey car.) to be stored in ```~/.ssh/id_mycar```:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAq7niQPKeCRrEugeDM1IHAHMdYPF0XFbcly8le6Lb6dR7U22s
VwlMS1k4c+s4x4HCZ+JR55BddL1WNrv2ix2YCqtbg28KI5Z+cyBdgrFi+KVuAse6
+QOgQR9g7RJkj+rCmie1mn0/3aQeFRdjdR4v1jFN4p0hb3apAahHV1HVZ2SInaq6
NX9RjAy0wEPSdiMknzJDRXS5nE67Jd9/jJdaowlWkyBc8kcEOuwkaPUOHgRuxKb+
bZVI599pFVtExJYBALnpfdTKo1spmRg5uQtWI82i7+/3nZA4sXnUXV2KWEtKkdM0
kjJwPgZ+EqWrOlLAuGCbO5FpS171rtkREGT4PQIDAQABAoIBAQCG3nuqxKGHxwVA
kYvib4bePIqTS682omWnOzj2DCcpU170XAthZAUOnGjw6Ylzbx7O1fm7oy8y80zV
ufPcuIZjwschx8CvyI9RPdcTQNvZKpvnBRR8Y/Olkc5fAvYF7buetJc1WS8ilLWn
nPHY1rd9QsXHt969mvULPy2gj73J7+rJAA4ED2uufvQ0xjh3BNMkBaYzynyjYZS/
g6b1RmCK+H1r+39SzXE3Gvayv53Yp9XpyM/J8tZ/UEdL2hoyvrFF1848TFlpQ0YB
9WU7euSdkKlLK8wVHaQGV8k9drYSiVWFDpGB/Jpxgr86oOJzv2ORQYYVBGYGbc9M
AiidVZDhAoGBANaVUNM2cme0phhwi24zP6PS4AH+yY9Z7nR6zque+0hWHe+aLj5d
goS87OPktVazVRJLoOrTPmrLSve85Fsp3Th3NW4Ol4ICRIu3LpxxUgV6huEFv+EI
3QBjPardqcr64pGij6ZIV/0VEnqiJn2u4Uf61r936JF9/exBho+8tj5pAoGBAMze
+JPPnos+FtB/HgXD54Qdx/xX/Q3zJPRS1zhr7zFDzDNO/FvV3TtlFojmYL+oIaDp
kwrmcDssXg68od/3Vk86AgmG5Cq261v9dbEmjw2kx2Cdmk4DTRHmIw6cIwpvsLYJ
unavhk2WmM1xgDtfk4PO/uMoTzULaqCfZ6j8CRi1AoGASxMomQz2j+P7LJfLoH2b
qWRw7SHIQTg0nloNDqxrvA4tIRQvU7CBppE2zDDLZQ8PF3yQSzgnIVQI4Y4b0u1d
sZC7h8rhJSJH+x3W1/MpwDLzF61cSY5BTA5sl+g/rH2EYXGfkozDBA+oTHGIx/Y0
aWuQUKLSIn0TJuJyAr4CgOkCgYB0aEUqB5B4YeEouvHeKMBFy340nfJFmOBoiyGL
B5kzjuhaRwkRTWWVOA0j4HMcs3XYLp/EU8d1d/JBwWDhF3LNNZKuwxymQKVe8ZeL
/vLNt9EpzqM8rJeAEhndVU57wZbQ+Jogkf9n2qgcI9/O3LG+9UDS5baL117QwYJu
/DZW+QKBgQCYM7SLmlqWbBFuBTxaX2oowZv3QYZUqlvPrQgFJ2WnqGesTOu8XhqT
0QbhbmqiTlsWKaiW2x+i1rHPaPmERq4uKCILbqjODzNt4XcnpNmcRcL/2uQGt566
6STt+8Ppw6W+mEBObjStr8i473vTc4Om0eqgLkPWpjG6Zgcg6Xnvdg==
-----END RSA PRIVATE KEY-----
```

## Changing the Name of the Car

Once SSH'ed into the car, edit the ```/etc/hostap/hostap.conf``` file by finding the
two lines and change the values to what you like:
```
ssid=LXLCar
wpa_passphrase=A2AutonomousVehicle
```
The ```channel=1``` may be changed to select a different channel for the Wi-Fi radio.
Only set it to 1, 6 or 11. A value of 0 (zero) or ```acs_survey``` for automatic
channel selection, but that is not tested.

The ```/etc/hostname``` file may also be changed to set the hostname in Linux.

(...to be continues...)
