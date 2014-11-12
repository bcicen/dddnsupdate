dddnsupdate
===========

dddnsupdate is a small CLI utility to dynamically nsupdate a nameserver based on discovered docker containers

Install
-----------

```
git clone git@github.com:bcicen/dddnsupdate.git
cd dddnsupdate/
python setup.py install
```

Usage
--------

The most typical use case is something like:
```
dddnsupdate --keyfile bind.key --zonename docker.mydomain.org --bindhost 1.2.3.4 --dockerurl tcp://1.2.3.5:4243
```
where bind.key is a TSIG format key like so:
```
key "docker.mydomain.org" {
    algorithm HMAC-SHA512;
    secret "<secret hash"";
};
```
