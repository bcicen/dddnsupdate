#!/usr/bin/python

import os, json
import dns.update
import dns.rdatatype
import dns.query
import dns.tsigkeyring
import dns.update
import dns.resolver
from dns.exception import DNSException, SyntaxError

from warnings import warn

class DockerDDNS(object):
    """
    """

    def __init__(self, api, bind_server, configfile):
        """
        Args:
            api: Docker Client instance used to do API communication
            bind_server: address of nameserver to update
            configfile: path to configfile
            zone: zonename to update
        """

        self.api = api
        self.bind_server = bind_server
        self.zone, self.kring, self.kalgo = self.getkey(configfile)

        try:
            print('connected to docker instance running api version %s' % \
                    self.api.version()['ApiVersion'])
        except docker.errors.APIError as ex:
            raise Exception(ex)

        cid_all = [ c['Id'] for c in self.api.containers() ]
	print('%s active containers' % len(cid_all))
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
        except:
            print k, 'is not a valid key. The file should be in DNS KEY \
                        record format. See dnssec-keygen(8)'
            exit()

        print('using keyring as:')
        print(k)
        return [zonename, keyring, algo]

    def nsupdate(self, cid):
        """
        """
        key_path = 'Name'

        try:
            cdic = self.api.inspect_container(cid)
        except docker.errors.APIError as ex:
            # 404 is valid, others aren't
            if ex.response.status_code != 404:
                warn(ex)
            return None

        cname = str(cdic[key_path].strip('/').replace('_', ''))
        cip = str(cdic['NetworkSettings']['IPAddress'])
        print(cip)
        if cip is not None:
            #instantiate updater for this transaction
            updater = dns.update.Update(self.zone, keyring=self.kring,
                    keyalgorithm=getattr(dns.tsig, self.kalgo))

            updater.add(cname, 30, 'A', cip)
            try:
                response = dns.query.tcp(updater, self.bind_server)
            except dns.tsig.PeerBadKey:
                print 'ERROR: The server is refusing our key'
                exit()
            print('Creating A record for %s with ip %s resulted in: %s' % 
                    (cname, cip, dns.rcode.to_text(response.rcode())))
