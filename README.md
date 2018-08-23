## About
`hueComposer` is a python script meant for running on a Raspberry Pi 3. It is under ongoing development for use by Robert Youds in an installation piece.

The basic goal is to provide a mechanism to drive 30+ Philips Hue lights.

A USB stick containing images is read by the script. The pixel values for each column of an image are stepped through in time, with the pixel values of each row being transmitted to each individual Philips Hue.

## Setup
### Automatic Setup
On a Raspberry Pi running [Linux Debian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/), run:

```
wget -O - https://raw.githubusercontent.com/sabjorn/hueComposer/master/scripts/install.sh | bash
```

### Manual Setup
#### Directory Location
This git should be put int:
```
/home/pi/
```
This will ensure that everything operates properly (hopefully).

#### TMPFS
Logs are stored in `/var/log` and over a long period of time this will cause a lot of writes to the SD card (which will damage it). To prevent writes to disk via logs, change the `/var/log` dir into a `tmpfs`.

**Note**: This will cause the logs to **NOT** persist between reboots. During development, it would likely be best to skip this step.

Run:
```
sudo vim /etc/fstab
```

and add:
```
tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0
```

Then reload by running:
```
sudo mount -a
```
#### USB
**NOTE**: This section is only needed for development since the files will be stored directly on the PI when deployed.

A FAT32 formatted USB stick is used. The images are stored on the top level.
FSTAB is used to automount the USB stick on boot. This way the Pi can be restarted and have different images loaded onto the stick for quick prototyping.

First, a directory must be made to mount to USB stick:
```
mkdir /home/pi/imgs
```

Next, FSTAB must be edited to automatically mount the USB stick on reboot. Only one USB stick will be used at a time and, since we want to be able to swap in any stick, the UUID will not be used for mounting--allowing any FAT32 formatted USB device to be mounted on startup:

edit `/etc/fstab`
```
sudo vim /etc/fstab
```

adding

```
/dev/sda1       /home/pi/imgs   vfat    nofail,uid=pi,gid=pi,rw    0       0
```

#### SystemD
Copy the `hueComposer.service` into the correct spot

```
sudo cp ./systemd/hueComposer.service /etc/systemd/system
```

then enable it

```
sudo systemctl daemon-reload
sudo systemctl enable hueComposer
```

This will make the `hueComposer` app run on boot. 

**OR**

service can be added with direct link:

```
sudo systemctl enable [absolute path]/hueComposer/systemd/hueComposer.service
```

## Dependencies
* Phue
* numpy
* matplotlib
* PILLOW

## To Do
Need some way to check which lights are actually available (which lights are plugged in and active)

Filenames for images can contain metadata (rate of play and transition time)


## Notes
* The IP address of the Hue should be locked on the router side.