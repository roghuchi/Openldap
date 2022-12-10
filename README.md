# Openldap

## Installation
### server side
configure FQDN hostname for your server

> sudo nano /etc/hosts


> 192.168.56.111   ldap.example.com


> sudo hostnamectl set-hostname ldap.example.com --static



Update Debian server

> sudo apt -y update


> sudo apt -y upgrade



Install OpenLDAP on Debian 11 / Debian 10 Linux

> sudo apt -y install slapd ldap-utils


> sudo dpkg-reconfigure slapd


Answer these questions:

omit openldap server configuration? No
DNS domain name? example.com
remove the database when slapd is purged? No
move old database? Yes


check ldap configuration:

> sudo slapcat


Add base dn for Users and Groups

> nano basedn.ldif

dn: ou=people,dc=example,dc=com 
objectClass: organizationalUnit
ou: people
dn: ou=groups,dc=example,dc=com
objectClass: organizationalUnit
ou: groups


apply basedn.ldif

> sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f basedn.ldif


Add User Accounts and Groups

Generate a password for the user account to add

> sudo slappasswd

sample output:

New password:
Re-enter new password:
{SSHA}5D94oKzVyJYzkCq21LhXDZFNZpPQD9uE


Create ldif file for adding users

> nano ldapusers.ldif

dn: uid=jmutai,ou=people,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: Josphat
sn: Mutai
userPassword: {SSHA}5D94oKzVyJYzkCq21LhXDZFNZpPQD9uE
loginShell: /bin/bash
homeDirectory: /home/jmutai
uidNumber: 3000
gidNumber: 300


apply ldapusers.ldif

> sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f ldapusers.ldif


Create ldif file for adding group

> nano ldapgroups.ldif

dn: cn=jmutai,ou=groups,dc=example,dc=com
objectClass: posixGroup
cn: jmutai
gidNumber: 3000
memberUid: jmutai


> sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f ldapgroups.ldif



### Install LDAP Account Manager on Debian 11 / Debian 10

Download the latest release of ldap account manager deb package

> wget http://prdownloads.sourceforge.net/lam/ldap-account-manager_7.7-1_all.deb


> sudo apt install -f ./ldap-account-manager_7.7-1_all.deb


Configure LDAP Account Manager on Debian 11 / Debian 10

check it on the web:

http://(server’s hostname or IP address)/lam
http://192.168.56.111//lam



### client side Debian 

> sudo apt update


> sudo apt install libnss-ldap libpam-ldap ldap-utils

Answer these questions:

LDAP server URI ? ldap://192.168.56.111/
Distinguished name of search base? dc=example,dc=com
LDAP version to use? 3
LDAP account for root? cn=admin,dc=example,dc=com
LDAP root account password? admin password (smile)
Allow LDAP admin account to behave like local root? Yes
Does the LDAP database require login? No
LDAP administrative account? cn=admin,dc=example,dc=com
LDAP administrative password? admin password (smile)

First edit nsswitch : (/etc/nsswitch.conf)

passwd:            compat ldap
group:               compat ldap
shadow:           compat ldap

Then edit these files :

/etc/pam.d/common-account

account sufficient pam_unix.so
account required pam_ldap.so

/etc/pam.d/common-auth

auth sufficient pam_unix.so nullok_secure
auth required pam_ldap.so use_first_pass
auth required pam_permit.so


 /etc/pam.d/common-password

password sufficient pam_unix.so nullok obsecure md5
password required pam_ldap.so

/etc/pam.d/common-session

session required pam_unix.so
session required pam_mkhomedir.so skel=/etc/skel umask=0022


Then restart nscd service

> /etc/init.d/nscd restart

Run this command and select all parameters:

> pam-auth-update --force


### client side Centos

> sudo yum update



> sudo yum install -y nss-pam-ldapd nscd openldap-clients


After install the packages you should run the below command for change configs:

authconfig-tui

in the next page you should enter ldap uri and base dn

also add these lines in this file:

> vi /etc/nslcd.conf


ldap_version 3
binddn cn=admin,dc=example,dc=com
bindpw [admin password]

Then restart nscd service

> service nslcd restart

Then add the line in this file for make home directory for the ldap users :

> /etc/pam.d/sshd

> session required pam_mkhomedir.so skel=/etc/skel umask=0022

Then restart sshd service

> service sshd restart


## Commands

> ldapsearch -x -D cn=admin,dc=test,dc=com -w [pass] -p 389 -h localhost

> ldapadd -x -D cn=admin,dc=test,dc=com -w  [pass] -p 389 -h localhost -f sshPublicKey.ldif

> ldapmodify -x -a -D cn=admin,dc=test,dc=com -w [pass] -p 389 -h localhost -f /etc/ldap/schema/ppolicy.ldif

## LSC configuration
http://lsc-project.org/
