# Turn ON/OFF Wifi over night

The following scheduled script activates/deactivates the wireless interface (WiFi) over night.
This script is intended to be used with Mikrotik devices with router OS 7.X or higher.

```bash
/system scheduler

add start-time="22:00:00" interval=24h on-event="/interface/wireless/disable [find]" name="Disable Wifi" comment="Turn OFF"
add start-time="06:30:00" interval=24h on-event="/interface/wireless/enable [find]" name="Enable Wifi" comment="Turn ON"

```