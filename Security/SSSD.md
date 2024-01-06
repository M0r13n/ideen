# SSSD



## Overlapping local and LDAP usernames

- local user accounts may conflict with LDAP usernames

- examples: *root* or *git*

- adjust `sssd.conf` and use the `filter_users` option:

  ```txt
  [nss]
  filter_groups = root,git
  filter_users = root,git
  reconnection_retries = 3
  entry_cache_timeout = 300
  entry_cache_nowait_percentage = 75
  ```

## Complex Configuration

```txt
[sssd]
config_file_version = 2
services = nss, pam, sudo
domains = LDAP

[nss]
# exclude root and git from the NSS database
filter_users = root, git

[pam]

[domain/LDAP]
id_provider = ldap
auth_provider = ldap
access_provider = ldap
sudo_provider = ldap
ad_hostname = sles15sp11.intern.priv
ldap_uri = ldap://ldap.example.com
ldap_search_base = dc=example,dc=com
ldap_user_search_base = ou=users,dc=example,dc=com
ldap_group_search_base = ou=groups,dc=example,dc=com
ldap_user_object_class = user
ldap_user_name = uid
ldap_group_object_class = posixGroup
ldap_group_member = memberUid
ldap_sudo_search_base = ou=sudoers,dc=example,dc=com
ldap_sudo_include_regexp = (memberOf=cn=Linux-Admins,ou=groups,dc=example,dc=com)

```

## Force TLS authentication

```txt
ldap_id_use_start_tls = True
cache_credentials = True
ldap_tls_cacertdir = /etc/openldap/certs
ldap_tls_reqcert = allow
```

## Group Policy Object Access Control

- [see](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/windows_integration_guide/sssd-gpo)

## Configuring simple Access Provider Rules

The `simple` access provider allows or denies access based on a list of user names or groups. It enables you to  restrict access to specific machines. 

```txt
[domain/your-domain-name]
access_provider = simple
simple_allow_users = user1, user2
simple_allow_groups = group1
```

## Configuring SSSD to Apply an LDAP Access Filter

When the `access_provider` option is set in `/etc/sssd/sssd.conf`, SSSD uses the specified access provider to evaluate which users are  granted access to the system. If the access provider you are using is an extension of the LDAP provider type, you can also specify an LDAP  access control filter that a user must match to be allowed access to the system.

```txt
[domain/your-AD-domain-name]
access provider = ad
ad_access_filter = (&(memberOf=cn=admins,ou=groups,dc=example,dc=com)(unixHomeDirectory=*))
```

## Generating access control reports using sssctl

`sssctl access-report idm.example.com`

`sssctl user-checks -a acct -s sshd example.user`

## Syntax Checker

You can test if the `/etc/sssd/sssd.conf` file on your host contains any typographical errors using the `sssctl config-check` command. 	

## Kerberos Tickets

If you install `krb5-user`, your AD users will also get a kerberos ticket upon logging in:

```
john@ad1.example.com@ad-client:~$ klist
Ticket cache: FILE:/tmp/krb5cc_1725801106_9UxVIz
Default principal: john@AD1.EXAMPLE.COM

Valid starting     Expires            Service principal
04/16/20 21:32:12  04/17/20 07:32:12  krbtgt/AD1.EXAMPLE.COM@AD1.EXAMPLE.COM
	renew until 04/17/20 21:32:12
```

Let’s test with *smbclient* using kerberos authentication to list he shares of the domain controller:

```
john@ad1.example.com@ad-client:~$ smbclient -k -L server1.ad1.example.com

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 
SMB1 disabled -- no workgroup available
```

Notice how we now have a ticket for the *cifs* service, which was used for the share list above:

```
john@ad1.example.com@ad-client:~$ klist
Ticket cache: FILE:/tmp/krb5cc_1725801106_9UxVIz
Default principal: john@AD1.EXAMPLE.COM

Valid starting     Expires            Service principal
04/16/20 21:32:12  04/17/20 07:32:12  krbtgt/AD1.EXAMPLE.COM@AD1.EXAMPLE.COM
	renew until 04/17/20 21:32:12
04/16/20 21:32:21  04/17/20 07:32:12  cifs/server1.ad1.example.com@AD1.EXAMPLE.COM
```

## PAM Access

By default, all users of the AD can login - if not limited by filters in ssd.conf. `pam_access` modules can be used to limit who can access the system:

```txt
# /etc/security/access.conf 
+:root:LOCAL
+:@IHRE_ADGRUPPE:ALL
+:gdm:LOCAL  # required for the graphical display manager
-:ALL:ALL
```

## Clear Cache

```bash
systemctl stop sssd
cd /var/lib/sss/db
rm -rf cache_*
systemctl start sssd
```

