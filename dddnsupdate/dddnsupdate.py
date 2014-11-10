#!/usr/bin/python

"""
CLI Utitility to send crafted nsupdate statement based on inspection of docker containers
Author: Bradley Cicenas <bradley.cicenas@gmail.com>
"""

import os,sys,argparse
from core import DockerDDNS
from . import __version__

docker_api_version='1.14'

def main():
    parser = ArgumentParser(description='dddnsupdate %s' % __version__)
    parser.add_argument('-v', action='version', version=__version__)
    parser.add_argument('-k', dest='keyfile', type=str, help='path to TSIG keyfile')
    parser.add_argument('-h', dest='bindhost', help='address of nameserver to update',
            default='127.0.0.1')
    parser.add_argument('-z', dest='zonename', help='zone name to be updated')
    parser.add_argument('-d', dest='docker_url', help='docker host to query', 
            default='unix://var/run/docker.sock')

    args = parser.parse_args()

    #simple validation
    if not args.keyfile:
        print('keyfile must be specified')
        sys.exit(1)

    if not args.zonename:
        print('zonefile must be specified(e.g. -z docker.mydomain.com)')
        sys.exit(1)

    try:
        kf = os.open(args.keyfile, 'r')
        kf.close()
    except Exception,e:
        raise Exception(e)

    docker_client = docker.Client(base_url=argpase.docker_url,
            version=docker_api_version, timeout=10)

    d_ddns = DockerDDNS(docker_client, argparse.bindhost,
                        argparse.keyfile, argparse.zone)

if __name__ == '__main__':
    main()
