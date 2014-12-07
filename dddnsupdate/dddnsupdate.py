#!/usr/bin/python

"""
CLI Utitility to send crafted nsupdate statement based on inspection of docker containers
Author: Bradley Cicenas <bradley.cicenas@gmail.com>
"""

import os,sys,docker
from argparse import ArgumentParser
from core import DockerDDNS
from . import __version__

docker_api_version='1.14'

def main():
    parser = ArgumentParser(description='dddnsupdate %s' % __version__)
    parser.add_argument('-v', action='version', version=__version__)
    parser.add_argument('--config', dest='configfile', type=str, help='path to config file')
    parser.add_argument('--bindhost', dest='bindhost', help='address of nameserver to update',
            default='127.0.0.1')
    parser.add_argument('--dockerurl', dest='docker_url', help='docker host to query', 
            default='unix://var/run/docker.sock')

    args = parser.parse_args()

    #simple validation
    if not args.configfile:
        print('--config must be specified')
        sys.exit(1)

    try:
        kf = open(args.configfile, 'r')
        kf.close()
    except Exception,e:
        raise Exception(e)

    docker_client = docker.Client(base_url=args.docker_url,
            version=docker_api_version, timeout=10)

    d_ddns = DockerDDNS(docker_client, args.bindhost, args.configfile)

if __name__ == '__main__':
    main()
