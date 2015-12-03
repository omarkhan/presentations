title: Forget Ansible - just write shell scripts
author:
  name: Omar Khan
  url: http://omarkhan.me/
controls: false
style: style.css

--

# Forget Ansible - just write shell scripts

--

### @\_\_omar\_\_

- Formerly backend lead at [Playlab Games](http://www.playlab.com/)
- Python developer for the last 7 years
- Mainly web development with django
- Currently working on the edX project
  - 92 Ansible roles (!)

--

# Why use Ansible?

## or Salt, Chef, Puppet...

--

### Why use Ansible?

- You want to deploy a service and its dependencies
- Example: a django web app
  - Python 2.7
  - Python requirements: django, celery, gunicorn, gevent...
  - PostgreSQL 9.4
  - Redis
  - Nginx

--

### Set everything up manually

- Spin up an EC2 instance running Ubuntu 14.04
- SSH in
- `apt-get install`
- Ubuntu 14.04 only has PostgreSQL 9.3. We want 9.4!
  - Add latest PostgreSQL package repo to `sources.list.d/`
  - `apt-get install` again
- Clone application repo
- `pip install -r requirements.txt`
- Edit configuration files (PostgreSQL, Nginx...)

--

### Set everything up manually

- Interactive
- Direct
- Easy

--

### Set everything up manually

But what if we need to set up a new server?

- Nobody remembers how to set it up anymore
- What if the original developer has disappeared?

--

![I have no idea what I'm doing](http://i2.kym-cdn.com/photos/images/original/000/234/765/b7e.jpg)

--

# The solution: automate it!

--

### Automate your server configuration

- Shell scripts
- Configuration management tools
  - Chef
  - Puppet
  - Salt
  - Ansible

--

### Shell scripts

```bash
#!/bin/bash

# Stop immediately if a command fails
set -e

# Add PostgreSQL 9.4 repo
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo 'deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main' |
  sudo tee /etc/apt/sources.list.d/postgresql.list

# Install packages
sudo apt-get update
sudo apt-get install -y python postgresql-9.4 redis-server nginx git

# Clone our repo
git clone https://github.com/omarkhan/app.git
cd app/

# Install python dependencies
sudo pip install -r requirements.txt
```

--

### Shell scripts

- Set up the server manually
- Copy-paste each command you run into the shell script
- Tidy up the script, document it
- Test it on a fresh server
- Commit it to your repo

--

### Advantages of shell scripts

- Not much more work than setting up the server manually
- Nothing new to learn
- We can set up new servers quickly - just run the script
- The script is documentation describing the server setup

--

### Disadvantages of shell scripts

- Bash can be ugly and hard to read (`esac` anyone?)
- Procedural rather than declarative
  - Procedural: **how** to set up the server
  - Declarative: **what** I want on the server
- Need to make sure our script is **idempotent**
  - We should be able to run the script many times on the same server without
    breaking anything

--

# Can we do better?

--

### Ansible

- Declarative server configuration
  - YAML + jinja2
- Comes with idempotent modules for most DevOps tasks
  - Installing packages (apt, yum...)
  - Installing python requirements (pip)
  - Copying configuration files
  - ...

--

### Ansible

```yaml
- hosts: all
  sudo: true
  tasks:
    - name: Add postgres apt key
      apt_key:
        url: https://www.postgresql.org/media/keys/ACCC4CF8.asc
    - name: Add postgres apt repo
      apt_repository:
        repo: deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main
    - name: Install packages
      apt: name={{ item }}
      with_items: [python-pip, postgresql-9.4, redis-server, nginx, git]
    - name: Clone git repo
      git: repo=https://github.com/omarkhan/app.git dest=/home/user/app/
    - name: Install python dependencies
      pip: requirements=/home/user/app/requirements.txt
```

--

# Is this better than the shell script?

--

### Advantages of Ansible

- Declarative
- Idempotent

--

### Declarative?

Is it really declarative?

- Ansible tries to turn YAML into a programming language
  - Conditionals
  - Loops
  - Modules
- Ansible tasks are run in order
  - We can't install postgresql-9.4 before adding the apt repo
- Our playbook is basically a list of commands

--

### Declarative?

If it's just a list of commands, why not just write the commands yourself?

- That way you know exactly what is going on
- If anything goes wrong, you are closer to the problem

--

### Debugging Ansible errors

```
TASK: [Add postgres apt repo] *************************************************
failed: [default] => {"failed": true, "parsed": false}
BECOME-SUCCESS-fmgfvvftrngmceouxmfppwportjsvwzp
Traceback (most recent call last):
  File "/home/vagrant/.ansible/tmp/ansible-tmp-1449127965.5-100195964141677/apt_repository", line 2855, in <module>
    main()
  File "/home/vagrant/.ansible/tmp/ansible-tmp-1449127965.5-100195964141677/apt_repository", line 464, in main
    cache.update()
  File "/usr/lib/python2.7/dist-packages/apt/cache.py", line 440, in update
    raise FetchFailedException(e)
apt.cache.FetchFailedException: W:Failed to fetch
http://apt.postgresql.org/pub/repos/apt/dists/trusty-pgdg/InRelease
Unable to find expected entry 'maindeb/binary-amd64/Packages' in Release file
(Wrong sources.list entry or malformed file)
, E:Some index files failed to download. They have been ignored, or old ones used instead.
OpenSSH_6.9p1, LibreSSL 2.1.7
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: Applying options for *
debug1: auto-mux: Trying existing master
debug1: mux_client_request_session: master session id: 2
Shared connection to 127.0.0.1 closed.


FATAL: all hosts have already failed -- aborting
```

--

### Ugly hacks

```yaml
# Install the python modules into {{ edxapp_venv_dir }}
- name : install python base-requirements
  # Need to use shell rather than pip so that we can maintain the context of our
  # current working directory; some requirements are pathed relative to the
  # edx-platform repo. Using the pip from inside the virtual environment
  # implicitly installs everything into that virtual environment.
  shell: >
    {{ edxapp_venv_dir }}/bin/pip install -i {{ COMMON_PYPI_MIRROR_URL }} --exists-action w -r {{ base_requirements_file }}
    chdir={{ edxapp_code_dir }}
  environment: "{{ edxapp_environment }}"
  sudo_user: "{{ edxapp_user }}"
  tags:
    - install
    - install:app-requirements
```

--

### Idempotency

Ansible beats our shell script here.

Idempotent:

```yaml
- name: Clone git repo
  git: repo=https://github.com/omarkhan/app.git dest=/home/user/app/
```

Not idempotent:

```bash
git clone https://github.com/omarkhan/app.git
```

--

### Idempotency

But it's easy enough to make our shell script idempotent:

```bash
[ -e app ] || git clone https://github.com/omarkhan/app.git
```

--

### Idempotency

Making shell scripts idempotent isn't that hard

- Use `mkdir -p`
- Add a few checks here and there
- Easier than learning Ansible!

--

### tl;dr

- Ansible (and similar tools) are supposed to improve on shell scripts by giving
  us a **declarative** and **idempotent** way to set up servers
- But Ansible playbooks are not really declarative
- And they can be very hard to debug
- The only remaining benefit is idempotency, which is easy enough to do in bash

--

### tl;dr

# Just write shell scripts!

--

# Debate!
