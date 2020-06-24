## Ansible Playbooks

Playbooks are a different way to use ansible from the ad-hoc examples we've looked at thus far. One of the reasons we labored through the manual steps of installing and configuring the software is because Ansible assumes you know what you are doing. So if your task reconfigures the nginx server, Ansible will not know that those tasks require the webserver to be restarted as a way of example. Thinking of Ansible playbooks as a an ordered series of tasks I want *played* on a remote host works for me. For those who have played American football the playbook reference is easier to get.  They are written in YAML and can be used to just about anything on a remote host.

### Ansible playbooks consist of

* Hosts
* Tasks
* Handlers (not always and better described with roles)

For our purposes the [hosts](ansible/inventory) are the machines we plan to manage. 


#### Playbook Preparation

* Create an ansible directory called `ansible` in the `controller` VM with the following steps:

```bash
vagrant ssh controller
mkdir ansible
cp -a /vagrant/ansible/* ansible/
chmod -R 755 ansible
```

Then switch into the ansible directory you just created and run the following playbooks with 

```bash
ansible-galaxy install -f -c -r requirements.yml
ansible-playbook -vvvvv playbook.yml
```

The first step uses `ansible-galaxy` which pulls roles from [Ansible Galaxy](https://galaxy.ansible.com/)
The second step uses `ansible-playbook` which runs a series of steps including pulling from roles

#### Tasks

An ansible task describes a state which shall be obtained on the machine. (I know!). That terrible sentence is better than using the word `idempotent` which is a good thing to remember about tasks. 

Tasks:
* do not mean machine X "go thou and do X" but rather,
* "machine X go and make sure X is done"
* Described in YAML, in a list. 
  * Each list item is a separate item executed sequentially
  * If any task fails, execution ends
* Tasks always have a name and a YAML dictionary name for the module the task is using

```yaml
- user:
   name: combine
   comment: "Combine User"
   groups: admin
   shell: /bin/bash
   password: "{{ ssh_password | password_hash('sha512') }}"
   update_password: on_create
```

* Tasks are sometimes conditional, or only run in some cases.
  * ... only if the host is bionic or xenial
  * ... only if postgresql version 10 was installed
* The *when* key takes an expression and skips the task if the expression is false


#### More Tasks

* Tasks should be idempotent whenever possible
* `Idempotency` means that running the task ensures the machine is in a certain state


#### More Tasks | Variables

* Ansible allows one to create variables within tasks. 
* enclosed "{{ between_curly_braces }}"
* uses [Jinja](https://palletsprojects.com/p/jinja/)

```yaml
...
- name: install latest version of a series of packages
  package:
    name: "{{ item }}"
    state: latest
  with_items: "{{ basic_packages }}"
```

#### More Tasks | Loops

* Ansible provides looping mechanisms 
* Since Ansible 2.5 `loop` is recommended over the `with_*` so instead of

```yaml
---
- hosts: all
  tasks:
  - name: band greetings that scale
    debug:
      msg: Hello, {{ item }}
    with_items:
      - code4lib
      - pittsburgh
```

use

```yaml
---
- hosts: all
  tasks:
  - name: band greetings that scale
    debug:
      msg: Hello, {{ item }}
    loop:
      - code4lib
      - pittsburgh
```
