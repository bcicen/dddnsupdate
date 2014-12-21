dddnsupdate
===========

dddnsupdate is a small CLI utility to dynamically nsupdate an existing BIND nameserver based on discovered docker containers

Getting Started
-----------

After setting up authenticated zone transfer and generating a TSIG key, modify the sampleconfig file to reflect your key, algorithm, and transfer zone.(a good tutorial can 
be found [here](http://honglus.blogspot.com/2011/04/authenticate-bind-zone-transfer-with.html))

Run dddnsupdate container with configfile mounted and any number of docker host addresses as arguments:
```
docker run -d -v /path/to/configfile:/config -e BIND_HOST=1.2.3.4 -e bcicen/dddnsupdate tcp://1.2.3.5:4243 tcp://1.2.3.6:4243
```

Usage
--------

Environmental variables:
 * BIND_HOST: Address of the nameserver to send zone updates to 
 * UPDATE_INTERVAL: Optional, how often to poll docker hosts and submit zone updates defaults to 60s. 

Configuration
--------

A configuration file is provided to dddnsupdate with the below required fields from a TSIG key:
```
{ 
  "zonename": "docker.mydomain.org.",
  "algorithm": "HMAC-SHA512",
  "secret": "<secret hash>"
}
```
