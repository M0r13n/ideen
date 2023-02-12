## Motivation

- reduce the number of hosts in a broadcast domain
- separate a physical network into multiple virtual networks
  - limit the number of hosts a given host can *see*
  - split hosts into different groups that share the same network
- improve security by adding virtual networks to isolate potential devices (e.g. IoT devices)
- improve documentation and traceability by separating hosts *by function* (**segmentation**)

## Solution

- VLAN = Virtual Logical Area Network = unique broadcast domain
- works on Layer 2
- 802.1Q is the trunking protocol used today

### 802.1Q

- every VLAN is assigned a unique number (12 bit) the **VLAN ID**
- devices can only communicate with devices that share the same VLAN-ID

#### Ethernet header

![header](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Ethernet_802.1Q_Insert.svg/1200px-Ethernet_802.1Q_Insert.svg.png)


- 802.1Q adds additional 4 bytes/32 bits to the Ethernet header:
  - **TPID** - 16 bits: Tag protocol identifier. always 8100. 
  - **TCI** - 16 bits:  Tag control information.
    - **PCP** - 3 bits: Priority Code Point
    - **DEI** - 1 bit:  Drop Eligible Indicator
    - **VID** - 12 bit: VLAN-Identifier  

### Terminology

- **Access port**: switch port that carries traffic for only one VLAN (untagged)
- **Trunk port**: switch port that carries traffic for multiple VLANs (tagged)
- **native VLAN**: by default frames **in this specific** VLAN are untagged when sent across trunk
- **Trunking**: carrying multiple VLANs over the same physical connection
