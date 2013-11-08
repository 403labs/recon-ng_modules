#Recon-ng Modules

[Recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng) does not allow for the use of third-party python module dependencies and sometimes modules aren't a good fit for the framework. Modules that can't get accepted into the Recon-ng framework will be hosted in this repo.

## ssl_san

This module will parse the SSL certificate for the provided URL and enumerate the subject alternative names.

### Usage


    recon-ng > use ssl_san_direct
    recon-ng [ssl_san_direct] > show options

      Name    Current Value     Req  Description
      ------  -------------     ---  -----------
      DOMAIN  www.verisign.com  yes  The host to check for subject alternative names (SAN)
      PORT    443               yes  The port to grab the SSL cert.
    recon-ng [ssl_san_direct] > set domain www.verisign.com
    DOMAIN => www.verisign.com
    recon-ng [ssl_san_direct] > run
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

### Installation

1. `easy_install m2crypto`
2. Clone this repo
3. `mkdir -p ~/.recon-ng/modules/discovery/info_disclosure/http/`
4. `cp recon-ng_modules/ssl_san_direct.py ~/.recon-ng/modules/discovery/info_disclosure/http/` or `ln -s recon-ng_modules/ssl_san_direct.py ~/.recon-ng/modules/discovery/info_disclosure/http/`

## brute_force_threaded
This is a rewrite of the built-in DNS brute forcing module to add multi-threading support.

### Usage

    recon-ng > use brute_force_threaded
    recon-ng [brute_force_threaded] > show options
    
      Name        Current Value         Req  Description
      ----------  -------------         ---  -----------
      ATTEMPTS    3                     yes  Number of retry attempts per host
      DOMAIN      example.com           yes  target domain
      NAMESERVER  8.8.8.8               yes  ip address of a valid nameserver
      THREADS     1                     yes  Number of threads
      WORDLIST    ./data/hostnames.txt  yes  path to hostname wordlist

    recon-ng [brute_force_threaded] > set domain example.com
    DOMAIN => example.com
    recon-ng [brute_force_threaded] > set threads 10
    THREADS => 10
    recon-ng [brute_force_threaded] > run

### Installation

1. Clone this repo
2. `mkdir ~/.recon-ng/modules/recon/hosts/gather/dns/`
3. `cp recon-ng_modules/brute_force_threaded.py ~/.recon-ng/modules/recon/hosts/gather/dns/` or `ln -s recon-ng_modules/brute_force_threaded.py ~/.recon-ng/modules/recon/hosts/gather/dns/`
