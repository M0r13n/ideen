# Netplan

- Backend-agnostic network configuration in YAML
- default in Ubuntu since 20.04
- [examples](https://github.com/canonical/netplan/tree/main/examples)
- [documentation](https://github.com/canonical/netplan/tree/main/doc)

## How to avoid duplicate default routes

In most examples there is a default route:

```yaml
routes:
  - to: default
	via: 192.168.1.1
```

This works fine as long as there is only one address/nic/gateway. More complex setups should only define a single default route. In this case, it makes sense to define additional routes like this:

```yaml
routes:
  - to: 192.168.99.0/24
    via: 10.0.1.1
```

Also, the `dhcp4-overrides` directive is quite useful to ignore the default route provided by the DHCP-server:

```yaml
dhcp4: true
dhcp4-overrides:
  use-routes: false
```

