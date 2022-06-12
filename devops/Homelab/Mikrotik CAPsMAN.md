# Configure Mikrotik CAPsMAN with CHATEAU and Audience

I am assuming that your Chateau has loaded it's default config. If so:

* bridge and lte interface are already configured correctly
* also the DHCP server is already setup (192.168.88.2 - 192.168.88.254)
* NAT is also already configured


## Setup CAPsMAN

I advise to interact with the Chateau via Winbox or SSH, because WebConfig does not support Copy&Paste.

### 2ghz

The following two commands, will add a CAPsMan config for the 2 GHZ band. It is considered best practise to use different SSIDs for bands to avoid clientside problems.

Create a configuration:

`caps-man configuration add country=germany datapath.bridge=bridge name=Config-2G security.authentication-types=wpa2-psk security.passphrase=top_secret security.encryption=aes-ccm security.group-encryption=aes-ccm datapath.client-to-client-forwarding=yes ssid=Furzkopf-2G channel.band=2ghz-b/g/n`

Explanation:

- `country=germany`: different countries have different regulations and frequencies. So choose your country.
- `datapath.bridge=bridge`: the access point is bind to the bridge interface named *bridge*
- `name=Config-2G`: the name of the configuration. choose any name, butmake sure you can distinguish your configs
- `security.authentication-types=wpa2-psk`:  choose wpa2-psk security. you may want to enable more insecure options like `wpa-psk` to support more client devices
- `security.passphrase=top_secret`: your passphrase used to connect to the WLAN
- `security.encryption=aes-ccm`: choose aes-ccm as encryption. alterntive would be tkip
- `datapath.client-to-client-forwarding=yes`: allow client to client communication. should be disabled in public wlans (hotel, coffee shop, etc)
- `ssid=Furzkopf-2G`: the ssid of the 2ghz network
- channel.band=2ghz-b/g/n`: the 2ghz channel

Create a provisioning rule:

`caps-man provisioning  add action=create-dynamic-enabled master-configuration=Config-2G hw-supported-modes=gn`

the important bits are:

- `action=create-dynamic-enable`
- `hw-supported-modes=gn`

Together these options make CAPSMAN assign SSIDs based on radio capabilities automatically.

You may refer to this post: https://forum.mikrotik.com/viewtopic.php?t=155048#p766920

### 5ghz

Create a configuration:

`caps-man configuration add country=germany datapath.bridge=bridge name=Config-5G security.authentication-types=wpa2-psk security.passphrase=top_secret security.encryption=aes-ccm security.group-encryption=aes-ccm datapath.client-to-client-forwarding=yes ssid=Furzkopf-5G channel.band=5ghz-n/ac`

This command is largely the same as the one for 2ghz. Just make sure to select the right channel: `channel.band=5ghz-n/ac`

Create a provisioning rule:

`caps-man provisioning add action=create-dynamic-enabled master-configuration=Config-5G hw-supported-modes=an,ac`


### Finally

 `/caps-man manager set enabled=yes`


## Connect Audience

Disconnect your Audience from power. Then press and hold the reset button. Plugin in power and keep on holding the reset button. Do yo until the green LED turns soldi green (stops flashing). This will enable 
**CAPs mode** and the device will automatically connect.

The Chateau itself comes with two wireless interfaces preconfigured. We do not want to used them. So make sure to disable them:

`interface disable [find  where type=wlan ]`

Afterwards, the CAP can be connected to the CAPsMAN (command based on this [wiki article](https://wiki.mikrotik.com/wiki/Manual:Simple_CAPsMAN_setup)):

`set bridge=bridge discovery-interfaces=bridge enabled=yes certificate=request lock-to-caps-man=yes interface=wlan1`

Now your Chateau router is both the CAPsMAN and a CAP, while every Audience device will be added as a new CAP.

## Optional

Enable auto certificates: `caps-man manager set ca-certificate=auto certificate=auto`

https://wiki.mikrotik.com/wiki/Manual:CAPsMAN#Manual_certificates_and_issuing_with_SCEP