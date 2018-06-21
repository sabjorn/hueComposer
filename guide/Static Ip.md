# System Overview

This system is comprised of three main components which communicate through standard TCP/IP networking layer. See figure 1.

While the build quality of all of the related components is quite high, there is always the possibility of failure (especially after a significant amount of time). Aside from any extreme cases, none of the components will ever damage the other components of the system. Repair information and equivalent replacement parts have been listed for each device below.

## Raspberry PI
### About
This is a small computer running the Linux operating system (`raspbian`). The OS runs off an SD card.

This component of the system is the brains behind the system. A Python program runs when the system is turned on (called `hueComposer`). This program sequences the lights of the system.

### Configuration

#### SD Card
The Raspberry PI's operating system as well as all the files necessary to run the installation are on the SD card. Data on the SD card may eventually corrupt and so a backup has been included with the archive (including instructions on how to properly copy the files onto the SD card)

#### Username and Password
The `Raspberry Pi` can be logged into by attaching a USB keyboard and an HDMI monitor. Or, if another computer with `SSH` capabilities is accessible, it is possible to `SSH` into the PI by connecting the computer to the router with an Ethernet cable.

This can be done with:

```
ssh pi@raspberrypi.local
```

or, if that fails, through the PI's static IP address:

```
ssh pi@192.168.0.101
```

The credentials for logging in in either way are:

Username: `pi`
Password: `raspberry`

### Equivalent
Any computer with the ability to run Linux, Python, and with a physical network adapter (ethernet port) should be able to run the software. The `hueComposer` source code is included in the archive and was designed to be relatively cross platform.

### Repair Information
If the Raspberry Pi does not boot, there are 3 possible problems:

First, the power supply may be failing. This will be quite noticeable if the LEDs on the PI do not flash when the power bar is started up. This can be easily replaced with a p

## Network Router
### About
The router is the device which connects the `Raspberry Pi` and the Philips Hue Hub together. This router is also

### Configuration
The current router is an older WiFi enabled router but the WiFi has been disable in the settings to prevent interference with other wifi networks and to prevent unauthorized access.

The `Raspberry Pi` and the `Philips Hue Hub` are assigned a static IP address through the router. For the `Hue Hub`, this allows the `hueComposer` software to easily communicate with the hub. The `Raspberry Pi`'s static IP address just reduces the difficulty of `SSH`ing into it if necessary. 

**Note**: If the `Hue Hub` is replaced with an equivalent model, this new Hub will have to be registered with the IP address of the previous hub through the router. Instructions for this are in a document called `Static IP` included with this documentation.  

#### Wiring
The `Raspberry Pi` and the `Philips Hue Hub` should each have an Ethernet cable connected into any of the ports on the router labeled `1` through `4`. The router will take care of the rest of the setup. 

#### Editing Router Settings
Router setting can be accessed by entering the IP address into a web browser: http://192.168.0.1/
The username is: `admin`
and the password is blank.

### Equivalent
Quite literally any router can be used for this purpose so long as the device supports `DHCP` and has at least 2 Ethernet jacks available. An `Ethernet switch` will not work though some modification to the `Raspberry Pi` since no IP addresses will be assigned to the `PI` or the `Hue Hub` and therefore not communication can take place. 

## Philips Hue Hub and Bulbs
### About
The colour controlled LED bulbs are made by Philips and require the Hue Hub to operate. The Hue Hub communicates to the bulbs with a Mesh Network protocol and the Raspberry Pi is able to communicate with the Hue Hub to orchestrate the changes in the colours of each bulb independently.

### Configuration
The Hue Hub must have a static IP address for communicating with the PI over ethernet. This is done on the router through [these steps](url).
Each Hue Bulb must be registered with the Hue Hub. This is not yet available through the application. Modifications of the code will be available in the future to support this capability. 

However, aside from physical damage to the LEDs, the bulbs should last a lifetime with moderate use.

### Equivalent
If the bulbs need to be replaced in the future, any existing wireless color controlled bulb should do. The `hueComposer` code will have to be modified in this case since the interface to lights other than the Philips Hue will be different. i.e. a different mechanism for communication with the new lights will have to be written. The code is written in such a way that this should actually be a trial matter.

## Power Bar
This device is not really considered part of the system and is just a mechanism for supplying AC power to all of the components of the system. If this device has any issues it can be replaced with any power bar which supplies enough power outlets.