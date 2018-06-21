# Replacing SD Card

The entire project has been compressed into a single image which can be copied onto an SD card and run on the Raspberry Pi 3.

These steps were all performed on Mac OSX 10.9.5. The steps should be similar on a Linux system but will require a little bit of digging. For Windows, hopefully by the time this document is needed windows will have completely turned into a Linux distro, otherwise there are some utilities you can download to perform this step (just google `copy linux distro to SD card windows` or something like that).

## Clone to SD Card
### Step 1:
Insert SD card into computer.
### Step 2:
Find SD card name. Run this command:

```
diskutil list
```

There should be a disk listed which matches the size of the SD card inserted. For example, `/dev/disk1`. Remember this, it will be necessary later.

### Step 3:
Unmount SD card.
Run this command with the disk name you found in the previous step.

```
diskutil unmountDisk /dev/disk#
```

### Step 4:
Copy the image onto SD card.
The image is saved as a `gzipped` archive and is included with this documentation.

Run this command to copy it properly onto the SD card.

```
sudo gzip -dc name!.img.gz | sudo dd of=/dev/rdisk# bs=1m
```

Making sure the `/dev/rdisk#` is replaced with the replacing with the disk number found in step 2. Note the `r` in front of `disk` for this command. This speeds up the operation.
