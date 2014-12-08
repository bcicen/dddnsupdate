#!/usr/bin/python

import os, json, logging
import dns.update
import dns.rdatatype
import dns.query
import dns.tsigkeyring
import dns.update
import dns.resolver
from dns.exception import DNSException, SyntaxError

from warnings import warn

logging.basicConfig(level=logging.INFO)

class DockerDDNS(object):
    def __init__(self, api, bind_server, configfile):
        """
        Args:
            api: Docker API Client instance
            bind_server: address of nameserver to update
            configfile: path to configfile
            zone: zonename to update
        """

        self.log = logging.getLogger()
        self.api = api
        self.bind_server = bind_server
        self.zone, self.kring, self.kalgo = self.getkey(configfile)

        try:
            self.log.debug('connected to docker instance at %s running api version %s' % \
                    (self.api.base_url, self.api.version()['ApiVersion']))
        except docker.errors.APIError as ex:
            raise Exception(ex)

        cid_all = [ c['Id'] for c in self.api.containers() ]
        self.log.info('%s running containers discovered at host %s' % \
                (len(cid_all), self.api.base_url))
        for cid in cid_all:
            self.nsupdate(cid)

    def getkey(self,filename):
        of = open(filename, 'r')
        dddnsconfig = json.load(of)
        of.close()
        zonename = dddnsconfig['zonename']
        algo = dddnsconfig['algorithm'].replace('-','_')
        key = dddnsconfig['secret']

        k = {zonename:key}
        try:
            keyring = dns.tsigkeyring.from_text(k)
        except :
            self.log.critical('Unable to create tsig keyring. The provided parameters should be \
                        taken from DNS KEY record format. See dnssec-keygen(8)')

        self.log.debug('created tsig keyring as: %s' % json.dumps(k))
        return [zonename, keyring, algo]

    def nsupdate(self, cid):
        """
        Args:
            cid: container ID to inspect and add to configured dns zone
        """
        key_path = 'Name'

        try:
            cdic = self.api.inspect_container(cid)
        except docker.errors.APIError as ex:
            # 404 is valid, others aren't
            if ex.response.status_code != 404:
                warn(ex)
            return None

        cname = str(cdic[key_path].strip('/').replace('_', '-'))
        cip = str(cdic['NetworkSettings']['IPAddress'])
        if cip is not None:
            #instantiate updater for this transaction
            updater = dns.update.Update(self.zone, keyring=self.kring,
                    keyalgorithm=getattr(dns.tsig, self.kalgo))

            updater.add(cname, 30, 'A', cip)
            try:
                response = dns.query.tcp(updater, self.bind_server)
            except dns.tsig.PeerBadKey as ex:
                self.log.critical('ERROR: The server is refusing our key')
                self.log.critical(ex)
            self.log.info('Updating record for container %s with IP %s: %s' % 
                    (cname, cip, dns.rcode.to_text(response.rcode())))
