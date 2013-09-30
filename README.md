#Recon-ng Modules

[Recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng) does not allow for the use of third-party python module dependencies. Modules that can't get accepted into the Recon-ng framework will be hosted in this repo. 

## ssl_san

This module will parse the SSL certificate for the provided URL and enumerate the subject alternative names.

## Usage


    recon-ng > use ssl_san
    recon-ng [ssl_san] > show options
    
      Name    Current Value     Req  Description
      ------  -------------     ---  -----------
      DOMAIN  www.verisign.com  yes  The host to check for subject alternative names (SAN)
      PORT    443               yes  The port to grab the SSL cert.
    recon-ng [ssl_san] > set domain www.verisign.com
    DOMAIN => www.verisign.com
    recon-ng [ssl_san] > run
    [*] www.verisign.com
    [*] verisign.com
    [*] www.verisign.net
    [*] verisign.net
    [*] www.verisign.mobi
    [*] verisign.mobi
    [*] www.verisign.eu
    [*] verisign.eu
    [*] forms.ws.symantec.com
    [*] sslreview.com
    [*] www.sslreview.com


### Required Python Modules 

* M2Crypto

### Installation Instructions

1. `easy_install m2crypto`
2. Clone the repo locally.
3. `cd recon-ng/modules/discovery/info_disclosure/http/`
4. `ln -s ~/.recon-ng_modules/ssl_san.py .`
