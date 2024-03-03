# How to regenerate SSH host keys on first boot?

Useful when creating operating system images.

Create a service file: `/etc/systemd/system/regenerate_ssh_host_keys.service`

```txt
[Unit]
Description=Regenerate SSH host keys
Before=ssh.service

[Service]
Type=oneshot
ExecStartPre=-/bin/dd if=/dev/hwrng of=/dev/urandom count=1 bs=4096
ExecStartPre=-/bin/sh -c "/bin/rm -f -v /etc/ssh/ssh_host_*_key*"
ExecStart=/usr/bin/ssh-keygen -A -v
ExecStartPost=/bin/systemctl disable regenerate_ssh_host_keys

[Install]
WantedBy=multi-user.target
```

Reload systemd:

`sudo systemctl daemon-reload`

Enable the service:

`sudo systemctl enable regenerate_ssh_host_keys.service`

This will create a run-once service that runs before starting the openssh-server. It then disables itself afterwards ([idea](regenerate_ssh_host_keys)) .