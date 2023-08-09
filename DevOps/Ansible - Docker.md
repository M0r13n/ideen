# Ansible with Docker

- possible to run Ansible playbooks in Docker containers
- useful for local testing or debugging
- define a simple Docker file with Ansible installed
    ```Dockerfile
    FROM ubuntu:jammy
    
    RUN apt-get update ; \
    apt-get install -y ansible; \
    apt-get clean
    ```
- define a simple playbook
	```Yaml
	---
    - name: Example Playbook
      hosts: all
	
      handlers:
        - name: restart chrony
          ansible.builtin.service:
            name: chrony
            state: restarted
	
      tasks:
        - name: Install chrony (NTP client)
          ansible.builtin.package:
            name: chrony
            state: present
          notify: restart chrony
          changed_when: true
	```
- run the playbook inside the container
	```bash
	#!/usr/bin/env bash
  
  IMAGE_NAME='ansible-2204-ubuntu'
  
  docker run --rm -v ${PWD}/example.yml:/foo/example.yml:ro ${IMAGE_NAME} ansible-playbook /foo/example.yml -i localhost, --connection=local
  ```