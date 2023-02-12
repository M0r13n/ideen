
## Why Ansible
- built by developers/sysadmins for developers/sysadmins
- easy to integrate existing shell scripts (e.g. [[Cheat Sheet|Bash]])
- run regular shell commands and is based purely on SSH
- there is no need to learn complex tools and languages like Chef or Puppet

## Cheat Sheet

### Terms
- **Node**: a system that is controlled by Ansible
- **Inventory File**: a file that contains information about server Ansible controls (default: `/etc/ansible/hosts` )
- **Playbook**: a file containing a set of tasks to be executed on the remote server
- **Role**: a collection of playbooks and files that are relevant to a goal (e.g. installing Docker)
- **Play**: a complete Ansible run

### Basic Commands
Test connectivity to hosts:
`ansible all -m ping`

Connect with a different user:
`ansible all -m ping -u some_user`

Use a custom SSH key:
`ansible all -m ping --private_key=~/.ssh/ansible`

Use passwords instead of SSH:
`ansible all -m ping --ask-pass`

Become root:
`ansible all -m ping --ask-become-pass`

or when using SSH

`ansible all -m ping -b`

Provide a custom inventory file:
`ansible all -m ping -i ./hosts.ini`

### Ad-hoc Commands
Syntax:

`ansible <HOSTS> -a <COMMAND>`

- `-a` stands for *ad-hoc*
- `-m` stand for *module*
- `-b` stand for become (e.g. become root)

Examples
- **Get disk space**: 
	- `ansible all -a "df -h"`
- **Get free disk space**
	- `ansible all -a "free -m"`
- **Install Python**:
	- `ansible docker -b -m apt -a "name='python3' state=present"`
- **Install pip**:
	-  `ansible docker -b -m package -a "name=python3-pip state=present"`
- **Install a package with pip**:
	- `ansible docker -b -m pip -a "name=bottle state=present"`
	- `ansible docker -b -m pip -a "name=bottle,pyais state=present"`
- **Upgrade system packages with APT**:
	- `ansible -m "apt" -a "update_cache=yes upgrade=yes" raspis -b`
- **Call a (Python) program**
	- `ansible docker -a "python3 -m bottle --version"`
- **Manage groups and users**:
	- `ansible docker -b -m group -a "name=test-group state=present"`
	- `ansible docker -b -m user -a "name=john state=present"`
	- `ansible docker -b -m user -a "name=john state=absent"`
	- `ansible docker -b -m group -a "name=test-group state=absent"`
- **Copy a file to a server**:
	- `ansible docker -m copy -a "src=./ansible.cfg dest='~/'"`
- **Retrieve a file from a server**:
	- `ansible docker -m fetch -a "src='~/ansible.cfg' dest='/tmp'"`
	- `ansible docker -m fetch -a "src='~/ansible.cfg' dest='/tmp/ansible.cfg' flat=yes"`
- **Delete a file or directory**:
	- `ansible docker -m file -a "dest='~/ansible.cfg' state=absent"`
- **Manage Cron jobs**:
	- `ansible docker -b -m cron -a "name=daily-cron hour=4 job='echo hi'"`
	- `ansible docker -b -m cron -a "name=daily-cron state='absent'"`

### Roles

Roles are collections of re-usable and shareable steps of execution. Unlike Playbooks roles itself are not executable. Instead, roles refine a set of tasks and additional files to configure a host for a certain *role*. Thus, the name role. Playbooks are more or less a mapping of roles and hosts. They are often used to combine multiple roles together to fulfill a specific purpose.

### Sample Playbooks

#### Regenerate SSH Host keys

```yml
--- 
# This playbook re-generates the SSH host keys 
- hosts: foo 
	become: true 
  tasks: 
    - name: Regen SSH host keys 
      block: 
        - name: "Delete existing host key files" 
          ansible.builtin.file: 
          path: "{{ item }}" 
          state: absent 
          with_fileglob: /etc/ssh/ssh_host_* 

        - name: "Regenerate host keys" 
          ansible.builtin.command: "dpkg-reconfigure openssh-server" 
          changed_when: true 
          environment: 
          DEBIAN_FRONTEND: noninteractive 

        - name: "Restart SSHD service" 
          ansible.builtin.service: 
          state: restarted 
          name: sshd
```
