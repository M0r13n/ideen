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



