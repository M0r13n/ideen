
## Why Ansible
- built by developers/sysadmins for developers/sysadmins
- easy to integrate existing shell scripts (e.g. [[Cheat Sheet|Bash]])
- run regular shell commands and is based purely on SSH
- there is no need to learn complex tools and languages like Chef or Puppet

## Cheat Sheet

### Terms
- **Node**: a system that is controlled by Ansible
- **Inventory File**: a file that contains information about server Ansible controls (default: `/etc/ansible/hosts` )
- **Playbook**: a file containing a set of tasks or roles to be executed on the remote server(s)
- **Role**: a collection of tasks and files that are relevant to achieve a goal (e.g. installing Docker)
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
- **Update packed without inventory**
  - `ansible -m package -a "update_cache=true upgrade=full" -e "ansible_user=pi" -i 10.0.0.240, 10.0.0.240 -k --become`


### Roles

Roles are collections of re-usable and shareable steps of execution. Unlike Playbooks roles itself are not executable. Instead, roles refine a set of tasks and additional files to configure a host for a certain *role*. Thus, the name role. Playbooks are more or less a mapping of roles and hosts. They are often used to combine multiple roles together to fulfill a specific purpose.

### How does it work?

Ansible uses the **Ansiballz** framwork. This framework contains boilerplate code such as argument parsing, formatting of return values as JSON. Parts of the module can be imported using `import from ansible.module_utils`.

When a module gets execute, Ansiballz constructs a zipfile – which includes the module file, files in `ansible/module_utils` that are imported by the module, and some boilerplate to pass in the module’s parameters. The zipfile is then Base64 encoded and wrapped in a small Python script which decodes the Base64 encoding and places the zipfile into a temp directory on the managed node. It then extracts just the Ansible module script from the zip file and places that in the temporary directory as well. Then it sets the PYTHONPATH to find Python modules inside of the zip file and imports the Ansible module as the special name, `__main__`. Importing it as `__main__` causes Python to think that it is executing a script rather than simply importing a module. This lets Ansible run both the wrapper script and the module code in a single copy of Python on the remote machine.

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

## Inventory

It is possible to assign a static IP to a given hostname by adding the following line to the inventory: `foo ansible_host=192.0.2.1`. Now, the host `foo` resolves to the ip `192.0.2.1`.
