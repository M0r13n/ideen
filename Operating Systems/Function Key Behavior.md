# Change Function Key behavior

## Preface

When using my Keychron or Apple Keyboard the function keys are in **media mode** by default. So, for example, pressing F12 does not open the developer menu in Chrome, but changes the current system volume. To access the regular `F-key` functionality, the `fn` key has to be pressed and held. 

## Change the Function key behavior

### Temporarily

The following line changes the Function key behavior until reboot:

`$ echo 2 | sudo tee /sys/module/hid_apple/parameters/fnmode`


### Permanently

Append the following line to `/etc/modprobe.d/hid_apple.conf` (you may need to create that file):

`options hid_apple fnmode=2`

After that run `sudo update-initramfs -u -k all` to copy the config file into the initramfs bootfile. Now, your Function keys behave as expected permanently.