# scarlettiger
Rutger Princeton DPLA Ansible Collab

# Learn to Automate with Ansible


## Overview

This will be a series of meetings to introduce [ansible](https://ansible.com) using the DPLA Combine Installer. The meetings will focus on getting to use ansible in a series of "lunches". The target audience is neophytes who are new to automating server administration with ansible. The structure of the meetings is to remain self-driven with some guidance. The nature of this repo will be a "live" document that will be improved on by those who find bits of it missing. Pull requests are therefore most welcome.

### Software Installation etc.,

Prior to arrival for the workshop make sure you have [Vagrant](https://vagrantup.com), [VirtualBox](https://virtualbox.org). At the time of creating the document there is a bug of the latest versions of vagrant and virtualbox working together. If you are unable to follow the [steps here](https://github.com/oracle/vagrant-boxes/issues/178) please create an issue on this repository so we can create a zoom session to help you correct this.

It is possible to use your UNIX-Like Operating System installation. To allow for consistency we will be using a virtual machines to allow for consistency. It is our experience that the less hoops one has to jump through when learning the easier it is to comprehend the scope and applicability of concepts. 

#### Installing Vagrant on Ubuntu/Debian Environments

One may find that installing Vagrant using `apt install vagrant` may install a Vagrant release older than 2.2.6. If you are in this situation, please use the following to install a more recent release of Vagrant:

```bash
sudo apt -y remove vagrant
# This is the latest stable release as of 03/08/20
curl -O https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
sudo apt install ./vagrant_2.2.6_x86_64.deb
```

Then please verify the version of Vagrant with:

```
vagrant --version
```

### Workshop materials

The overall [agenda is here](AGENDA.md)

