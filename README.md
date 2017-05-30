##About
`hueComposer` is a python script meant for running on a Raspberry Pi 3. It is under ongoing development for use by Robert Youds in an installation piece.

The basic goal is to provide a mechanism to drive 30+ Philips Hue lights.

A USB stick containing images is read by the script. The pixel values for each column of an image are stepped through in time, with the pixel values of each row being transmitted to each individual Philips Hue.

##Setup
###Directory Location
This git should be put int:
```
/home/pi/
```
This will ensure that everything operates properly (hopefully).

###USB
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

###Upstart
There is a `.conf` file in the `Upstart` directory in this git. Copy that file to `/etc/init/`. As long as Upstart is installed on the system this should get the Python script to run after reboot.

There is a good guide on Upstart [here](https://www.digitalocean.com/community/tutorials/the-upstart-event-system-what-it-is-and-how-to-use-it).

##Dependencies
* Phue
* numpy
* matplotlib
* PILLOW

##To Do
Need some way to check which lights are actually available (which lights are plugged in and active)

Filenames for images can contain metadata (rate of play and transition time)


## Notes
* The IP address of the Hue should be locked on the router side.