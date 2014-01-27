# ssl_san.py - a Recon-ng module
# Author: Zach Grace (ztgrace) zgrace@403labs.com
# Copyright (c) 2013 403 Labs, LLC <http://www.403labs.com>
# License: GPLv3
#
# ssl_san.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ssl_san.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# See <http://www.gnu.org/licenses/> for a copy of the GNU General
# Public License

import framework
# unique to module
import ssl
from M2Crypto import X509

class Module(framework.Framework):

    def __init__(self, params):
        framework.module.__init__(self, params)
        self.register_option('domain', None, 'yes', 'The host to check for subject alternative names (SAN)')
        self.register_option('port', 443, 'yes', 'The port to grab the SSL cert.')
        self.info = {
                     'Name': 'SSL SAN Lookup',
                     'Author': 'Zach Grace (@ztgrace) zgrace@403labs.com',
                     'Description': 'This module will parse the SSL certificate for the provided URL and enumerate the subject alternative names',
                     'Comments': []
                     }

    def module_run(self):
        domain = self.options['domain']['value']
        port = self.options['port']['value']
        try:
            cert = ssl.get_server_certificate((domain, port))
        except:
            self.error('Unable to retrieve SSL certificate from %s:%s' % (domain,port))
            return

        # fix the cert format for M2Crypto
        cert = cert.replace(ssl.PEM_FOOTER,'\n%s' % ssl.PEM_FOOTER)
        x509 = X509.load_cert_string(cert)
        sans = x509.get_ext('subjectAltName').get_value()
        sans = sans.replace('DNS:', '')
        for name in sans.split(', '):
            self.alert(name)
