#### Pipelining

```ini
[ssh_connection]

pipelining = True
```

By default, Ansible executes tasks by copying a file onto the remote host, executing it and reporting the results back to the control machine. By using pipelining Ansible can execute commands directly through a persistent SSH session.

#### Static Analysis

```bash
#  ensure the YAML is properly formatted
yamllint .
# ensure the playbooks follow best practices
ansible-lint .
# ensure that the YAML is syntactically compatible to Ansible
ansible-playbook . --syntax-check
# pretend to execute the playbook
# modules report what they would have changed
# modules need to support check mode
# otherwise they are ignored
ansible-playbook . --check
# provide a before and after comparison
# can be used together with --check to show what would have been changed
ansible-playbook . --check
```

#### Configure .ini files

```yaml
---
- xrdp_configuration:
  - option: crypt_level
    section: Globals
    value: high
    
- name: Configure xrdp
  community.general.ini_file:
    path: /etc/xrdp/xrdp.ini
    section: "{{ item.section }}"
    option: "{{ item.option }}"
    value: "{{ item.value }}"
    mode: "0644"
  loop: "{{ xrdp_configuration }}"
  loop_control:
    label: "{{ item.option }}"
```

#### Ufw with items

```yaml
- name: Allow RDP access through firewall (Port 3389, 3350) 
  become: true 
  ansible.builtin.ufw: 
	rule: "{{ item.rule }}" 
	port: "{{ item.port }}" 
	proto: "{{ item.proto }}" 
  notify: 
	- restart ufw 
  with_items: 
    - {rule: 'limit', port: '3389', proto: 'tcp'} 
    - {rule: 'limit', port: '3350', proto: 'tcp'} 
```

#### Create a new virtual environment

```yaml
- name: Create a new virtual environment
  ansible.builtin.pip: 
    requirements: /path/to/requirements.txt
    virtualenv: /path/to/venv 
    virtualenv_python: python3 
    extra_args: --no-cache-dir  # can be useful for service users without a home dir
```


#### Become a different user

```yaml
become: true 
become_user: "foobar" 
```

#### Create a service user

```yaml
- name: Create the service user
  become: true 
  ansible.builtin.user: 
    name: foobar
    system: true 
    shell: "/usr/sbin/nologin"  # forbid login
    createhome: false   # no home dir
    password: '!'  # locked/disabled password on Linux systems
```

#### Clone a private repo

Git requires authentication to clone private repos. It is near impossible to provide such credentials to the remote machine without accidentally leaking one password or private key. A workaround is to clone the repo on the primary host and to copy the cloned folder to the remote host afterwards. This assumes that the primary host is authenticated to clone the repo (e.g. SSH keys).

```yaml
- name: Clone the project locally 
  delegate_to: localhost 
  ansible.builtin.git: 
    repo: "{{ URL }}" 
    dest: /tmp/folder
    version: master 
  notify: copy-git-folder 
```

```yaml
- name: Copy repo to the remote
  become: true 
  ansible.builtin.copy: 
    src: /tmp/folder
    dest: /path/to/remote
```

#### Mount a cifs drive

```yaml
- name: "Mount /foo 
  become: true 
  ansible.posix.mount: 
    src: "//10.0.0.1/foo" 
    path: /mnt/foo 
    opts: rw,exec,sync,nofail,guest,file_mode=0555,dir_mode=0555 
    state: mounted 
    fstype: cifs
```

#### Delete files while ignoring some

```yaml
- name: Capture motd files to delete 
  find: 
    paths: /etc/update-motd.d/ 
    file_type: file 
    excludes: 
      - "01-neofetch" 
      - "10-help" 
 register: found_files 

- name: Remove annoying Ubuntu messages 
  become: true 
  file: 
    path: "{{ item.path }}" 
    state: absent 
  with_items: "{{ found_files['files'] }}"
```
