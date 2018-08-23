#!/usr/bin/env bash
if [ "$(whoami)" != "root" ]; then
    echo "must be run as root."
    exit 1
fi

set -ex
## Add all dependencies
buildDeps="python-pip python-imaging python-scipy python-numpy python-dev python-setuptools python-wheel omxplayer dnsmasq git vim"
until apt-get update 
do
  echo "apt-get update failed, trying again."
  sleep 1
done
apt-get install -y $buildDeps --no-install-recommends
rm -rf /var/lib/apt/lists/*

# setup hueComposer
if [ -z "$1" ]
  then
    GITBRANCH="master"
  else
    GITBRANCH="$1"
fi

cd ${HOME}
git clone -b $GITBRANCH https://github.com/sabjorn/hueComposer.git
cd ./hueComposer
pip install -r requirements.txt
systemctl enable ${HOME}/hueComposer/systemd/hueComposer.service

## Setup Hostname
HOSTVAR="${HOSTVAR:-huecomposer}"
echo ${HOSTVAR} > /etc/hostname

## Enable SSH
systemctl enable ssh

# Consider doing this instead:
# https://raspberrypi.stackexchange.com/questions/78787/howto-migrate-from-networking-to-systemd-networkd-with-dynamic-failover

## Setup default WIFI
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CA

network={
    ssid=\"house-catsle\"
    psk=3cd725e65d69d40b9643ddc556c3e8a3574255c4b867c721e47b5a045cb435ed
}" > /etc/wpa_supplicant/wpa_supplicant.conf
#systemctl enable wpa_supplicant

## Setup routerless Hue Hub connection (ethernet directly to Hub)
# setup DHCPCD
echo "interface eth0
static ip_address=192.168.220.2/24
static routers=192.168.220.1
static domain_name_servers=192.168.220.1
metric 300

interface wlan0
metric 200" >> /etc/dhcpcd.conf
# NOTE: metric changes priority of wlan0 over eth0
#systemctl daemon-reload
# systemctl restart dhcpcd

# setup DNSMSQ
echo "interface=eth0
listen-address=192.168.220.1
dhcp-range=192.168.220.50,192.168.220.150,12h" >> /etc/dnsmasq.conf
#systemctl daemon-reload
# systemctl restart dnsmasq

## setup /var/log to be tempfs
echo "tmpfs /var/log tmpfs defaults,noatime,nosuid,mode=0755,size=100m 0 0" >> /etc/fstab
mount -a

set +ex