# What is a network?

* a network is used to share **resources** between devices
	* e.g. makes a printer available to multiple devices
	* therefore not every device needs to have it´s own printer
	* instead, many devices can share a single printer
* a network is also used to **interchange data/information** between devices
* every participant in the network is called a *node*
* such *nodes* are connected through a data-link
	* Ethernet (today)
	* Serial (in the older days)

## What is a server?
* *a server is a device that provides functionality to clients*

## What is a client?
* *a client is a device that accesses the functionality provided by a server*
* this usually happens over a network

```mermaid
graph LR
Server ---|network| Client
```

-> servers and devices communicate through protocols
	* protocols define the rules that allow two or more entities to exchange information
	* just like we use different languages (English, German, French) to communicate
-> servers can speak multiple languages (protocols) by listening on multiple ears (ports)
	* but each ear can only understand a single language

## Terms

- WAN: Wide Area Network
- LAN: Local Area Network
- bridge vs switch
	- a bridge learns MAC addresses in software
	- a switch learns MAC addresses in hardware (ASIC)
* Layer-1 devices: *dump* devices that operate on the electronic layer (forward electric signals)
* Layer-2 devices: understand Ethernet frames and use MAC addresses to send frames
* Layer-3 devices: route packets on the [[TCP-IP-Model|IP layer]] (one layer above Ethernet)