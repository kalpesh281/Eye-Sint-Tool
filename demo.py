#!/usr/bin/env python3

import os
import sys
from json import loads
import tldextract
import ipaddress
import datetime
import socket
import settings as config
import argparse


def demo1():
    # target = (input("Enter URL : "))
    # config default
    home = config.home
    usr_data = config.usr_data
    conf_path = config.conf_path
    path_to_script = config.path_to_script
    src_conf_path = config.src_conf_path
    meta_file_path = config.meta_file_path

    parser = argparse.ArgumentParser(
        description=f'Eye-Sint')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('--headers', help='Header Information',
                        action='store_true')
    parser.add_argument(
        '--sslinfo', help='SSL Certificate Information', action='store_true')
    parser.add_argument('--full', help='Full Recon', action='store_true')
    parser.add_argument('--whois', help='Whois Lookup', action='store_true')

    ext_help = parser.add_argument_group('Extra Options')

    ext_help.set_defaults(
        # sp=config.ssl_port,
        o=config.export_fmt
    )

# https://www.bvmengineering.ac.in/ --headers

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit()

    target = (input("Enter URL : "))
    print(f"Your provided URL : {target}")

    # headers =
    print("""Options available 
    
            1. Headers
            2. SSL information
            3. Whois Lookup
            4. web-crawl
            """)
    a = int(input("Enter option : "))

    # print(headinfo)
    # sslinfo = args.sslinfo

    sslp = 443
    full = args.full
    output = args.o

    type_ip = False
    data = {}

    def full_recon():
        from modules.sslinfo import cert
        from modules.headers import headers
        headers(target, output, data)
        cert(hostname, sslp, output, data)

    try:

        if target.startswith(('http', 'https')) is False:
            print(
                f'Protocol Missing, Include http:// or https:// \n')
            sys.exit(1)
        else:
            pass

        if target.endswith('/') is True:
            target = target[:-1]
        else:
            pass

        print(f'Target : {target}')
        ext = tldextract.extract(target)
        domain = ext.registered_domain
        hostname = '.'.join(part for part in ext if part)

        try:
            ipaddress.ip_address(hostname)
            type_ip = True
            ip = hostname
        except Exception:
            try:
                ip = socket.gethostbyname(hostname)
                print(f'\nIP Address : {str(ip)}')
            except Exception as e:
                print(f'\nUnable to Get IP : {str(e)}')
                sys.exit(1)

        start_time = datetime.datetime.now()

        if output != 'None':
            fpath = usr_data
            # dt_now = str(datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S'))
            dt_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            fname = f'{fpath}fr_{hostname}_{dt_now}.{output}'
            # respath = f'{fpath}fr_{hostname}_{dt_now}'
            # respath = os.path.join(fpath, f'fr_{hostname}_{dt_now}')

            respath = os.path.join(fpath, f'fr_{hostname}_{dt_now}')
            if not os.path.exists(respath):
                try:
                    os.makedirs(respath)
                except OSError as e:
                    print(f"Error creating directory: {e}")
            # if not os.path.exists(respath):
            #     os.makedirs(respath)
            output = {
                'format': output,
                'directory': respath,
                'file': fname
            }

        if full is True:
            full_recon()

        if (a == 1):
            from modules.headers import headers
            headers(target, output, data)

        if (a == 2):
            from modules.sslnew import ssl_analyzer
            result = ssl_analyzer(
                target, output, data)
            # print(result)

        if (a == 3):
            from modules.whois import whois_lookup
            whois_lookup(ip, output, data)

        if (a == 4):
            from modules.crawler import crawler
            crawler(target, output, data)

        else:
            pass

        # if any([headinfo]) is not True:
        #     print(
        #         f'\nError : At least One Argument is Required with URL')
        #     output = 'None'
        #     sys.exit(1)

        end_time = datetime.datetime.now() - start_time
        print(f'\nCompleted in {str(end_time)}\n')
        print(f'Exported : {respath}')
        sys.exit()
    except KeyboardInterrupt:
        print(f'Keyboard Interrupt.\n')
        sys.exit(130)
