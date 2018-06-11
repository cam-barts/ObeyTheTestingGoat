# Provisioning a New Site

### Required Packages

* nginx
* Python 3.6
* virtualenv
* pip
* git

_Example on Ubuntu:_
```shell
user@machine:~$ sudo add-apt-repository ppa:fkrull/deadsnakes
user@machine:~$ sudo apt-get install nginx git python3.6 python3.6-venv
```


### Nginx Virtual Host Config
* See [Nginx Template](./nginx.template.conf)
* replace _SITENAME_ with appropriate site name and _USERNAME_ with appropriate user name

### Systemd Service
* See [Service Template](./gunicorn-systemd.template.service)
* replace _SITENAME_ with appropriate site name and _USERNAME_ with appropriate user name

### Example Folder Structure
_Assuming we have user account "user"_

```
/home/user
  |--sites
      |--SITENAME
          |--database
          |--source
          |--static
          |--virtualenv
```
