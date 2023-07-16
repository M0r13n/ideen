# cloud-init

**cloud-init** is used to configure cloud images (operating systems templates). It customizes **identical clones** automatically:

- set default locale
- set hostname
- generate SSH host keys
- setting up ephemeral mount points

During boot, `cloud-init` identifies the cloud it is running on and initialises the system accordingly. Cloud instances will automatically be provisioned during first boot with networking, storage, SSH keys, packages and various other system aspects already configured.

**Configuration directory**: Anything defined in `/etc/cloud/cloud.cfg` and `/etc/cloud/cloud.cfg.d`.


## Example(s)

- https://github.com/canonical/cloud-init/tree/main/doc/examples
- [Ansible managed](https://github.com/canonical/cloud-init/blob/main/doc/examples/cloud-config-ansible-managed.txt)
- https://cloudinit.readthedocs.io/en/latest/reference/examples.html

## Misc

- [Ubuntu Cloud Images](https://cloud-images.ubuntu.com/)

## VMWare

The following steps prepare a virtual machine template for customization with raw cloud-init data.

1. Install required tools:
```bash
$ sudo apt update
$ sudo apt install open-vm-tools
$ sudo vmtoolsd -v
$ sudo systemctl is-enabled open-vm-tools.service
```

1. Prepare cloud-init
```bash
$ sudo apt update
$ sudo apt install cloud-init
$ sudo cloud-init -v
$ sudo systemctl is-enabled cloud-init.service
$ sudo systemctl is-enabled cloud-init-local.service
```  
2. Configure cloud-init to accept the OVF data source: `datasource_list: [ NoCloud, ConfigDrive, Azure, OVF, OpenStack, Ec2 ]`
4. Configure cloud-init to enable VMware customization with raw cloud-init data.
	- edit `/etc/cloud/cloud.cfg`:
	```yaml
	disable_vmware_customization: true
    datasource:
      OVF:
        allow_raw_data: true
    vmware_cust_file_max_wait: 25
	```
5. Run the cloud-init clean step to remove any artifacts from previous configuration failures: `$ sudo cloud-init clean`
6. `$ sudo poweroff`