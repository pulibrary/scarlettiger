## Ansible Introduction

Before installing ansible we will need to configure the controller VM to connect to `dplanode1`. Ansible uses ssh to connect to the other virtual machines. When you ran `vagrant up` it generated `{centos,ubuntu}_keys.txt` files at the root of the directory. We will be copying the contents of root@controller generated keys into the dplanode1 virtual machine. (Details on how these keys were generated are in the shell script inside the vagrantfiles). If you have run vagrant up a number of times then it is the `root@controller` towards the bottom of the file.

```bash
vagrant ssh dplanode1
vagrant@dplanode1:~$ cat /vagrant/ubuntu_keys.txt
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDhXqe2Ja0ato4eG+kCUSuGUTKm57SakdQGO7k0lJHJYgUU0QUB/IByhvA2teiJj2+F3WgiU3Pl9U/QCvTMswRGTcvjEFvGPOGJZfVCiQ+L8zQa9QM1f11tSAXM3mqIIPFUVNHqp42F8w04Q10rVw21eCVXoNSGQzbUIPRyMmHEq6ZDOUwGeH7l0aXzr70tu85XcL5jnoh7adb1y3GAMT7SkESsg05lzs7EpzYMBR+/vwT8YOiqOUScnOhiMJwX1ae2Ztw7rDPh2aoDmXHtF5B5hPmzMN8rlv6yCbDEEvIWhJtD4/B0j+GPpQKWyXrryQHuFu++3634Ck1B1c3eEDaX root@controller
```

Log into the controller VM with and let's install Ansible and confirm installation with the following commands:

```bash
vagrant ssh controller
```

On Ubuntu

```bash
sudo apt-get -y install vim ansible
which ansible
```

On Centos

```bash
sudo yum -y install vim ansible
which ansible
```

Confirm that we can log into all the other nodes with 

```bash
ssh 10.0.15.11
```

### Hello Ansible

The simplest command for ansible is a *local command.* Typically on your controller node or local computer. Here is the verbose full command

```bash
ansible all --inventory "localhost," --module-name debug --args "msg='Hello World'"
```

The `ansible` is the name of the executable and we are running ansible against all machines on our `inventory` in this case one using the module name `debug` which echoes to stdout the arguments message `Hello World`. The shortcut for that command which we will be using from here on is

```bash
ansible all -i "localhost," -m debug -a "msg='Hello World'"
localhost | SUCCESS => {
    "msg": "Hello World"
}
```


```bash
ansible all -m shell -a "ping -c 3 localhost"
```

is functionally the same with

```bash
ansible all -m ping
```

The latter has guaranteed idempotency in a way that the former does not. 

Finally let's install the nginx webserver software again by passing ansible's verbose:

```bash
ansible -vvv all -i "10.0.15.11," -m package  -a "name=nginx state=present" -b
```

this will use the ansible module `package` to uninstall and install the nginx webserver software, the `-b` flag elevates our privilege. Feel free to uninstall and install the software that the manual steps we did earlier did before we move on to configuring ansible and reducing the number of ansible flags to remember.

The first step is run and ansible does nothing because nginx is already installed, the second one removes it. The first step is a key property of idempotence where ansible only does what needs to be done. So nginx was already installed so ansible did nothing.

### Configure Ansible

Thus far we have called individual VMs by their respective IP addresses. The examples presented thus far are useful but become impractical fairly quickly. Generally ansible is used against multiple hosts on your infrastructure at the same time. These are defined in an `INI` (YAML is okay also) format file. The default location is usually `/etc/ansible/hosts` which you can examine for pattern examples. The documentation on [inventory patterns](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#intro-inventory) is discussed on Ansible's brilliant documentation. The warnings we saw earlier when you ran the ping command are because by default ansible will look at the default `/etc/ansible/ansible.cfg`. We will modify this by using the file under `ansible/ansible.cfg` this will include the hosts we will be connecting to for the rest of the workshop.

If you run the following steps you will see ansible use the `/etc/ansible/ansible.cfg` first:

```bash
vagrant ssh controller
ansible all -m ping
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
```

If you cd into `/vagrant/ansible` you get a different result because ansible picks the inventory defined in `ansible.cfg`

```bash
cd /vagrant/ansible
ansible all -m ping
10.0.15.11 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
10.0.15.11 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

From this directory let's run a few more commands from the [Ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html) on all the VMs

```bash
ansible all -m shell -a 'date'
ansible all -m shell -a 'uptime'
```
Those are the using the shell module to run the `date` and `uptime` commands on all the VMs

```bash
ansible all -m package -a "name=rsync state=present" -b
```
installs rsync on all servers

```bash
ansible all -m package -a "name=rsync state=absent" -b
```
uninstalls rsync on all servers

```bash
ansible dplanodes -m user -a "name=conan password=s3kr1t-455 comment='Conan theDeployer'" -b
```
adds the user `conan` on the dplanodes group

```bash
ansible dplanodes -m user -a "name=conan state=absent" -b
```
removes the user
```bash
ansible webserver -m service -a "name=nginx state=restarted" -b
```
restarted the nginx webserver on the webserver group
```bash
ansible all -m setup
```
presents all the information about all the VMs

## Exercise

* use ansible's [copy module](https://docs.ansible.com/ansible/latest/modules/copy_module.html) to copy the `{centos,ubuntu}-keys.txt` to all the VMs.
* use ansible's [service module](https://docs.ansible.com/ansible/latest/modules/service_module.html) to restart the postgresql server
