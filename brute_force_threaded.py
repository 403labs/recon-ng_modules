import framework
# unique to module
import dns.resolver
import os.path
import threading
import Queue

class DNSBrute(threading.Thread):
    def __init__(self, framework, wordQ, foundQ, newQ, domain, resolver, max_attempts):
        threading.Thread.__init__(self)
        self.framework = framework
        self.wordQ = wordQ
        self.foundQ = foundQ
        self.newQ = newQ
        self.domain = domain
        self.resolver = resolver
        self.max_attempts = max_attempts
        self.kill = False

    def run(self):
        while not self.kill or self.wordQ.empty():
            word = self.wordQ.get()

            attempt = 0
            while attempt < self.max_attempts:
                host = '%s.%s' % (word, self.domain)
                if self.framework.global_options['debug']: self.framework.output("Checking host: %s" % host)
                if self.framework.global_options['debug']: self.framework.output("wordQ length: %s" % self.wordQ.qsize())
                try:
                    answers = self.resolver.query(host)
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    self.framework.verbose('%s => Not a host.' % (host))
                except dns.resolver.Timeout:
                    self.framework.verbose('%s => Request timed out.' % (host))
                    attempt += 1
                    continue
                else:
                    # process answers
                    for answer in answers.response.answer:
                        for rdata in answer:
                            if rdata.rdtype == 1:
                                self.framework.alert('%s => (A) %s - Host found!' % (host, host))
                                if self.framework.add_host(host):
                                    self.newQ.put(host)
                                self.foundQ.put(host)
                            if rdata.rdtype == 5:
                                cname = rdata.target.to_text()[:-1]
                                self.framework.alert('%s => (CNAME) %s - Host found!' % (host, cname))
                                if host != cname:
                                    if self.framework.add_host(cname):
                                        self.newQ.put(cname)
                                    self.foundQ.put(cname)
                                if self.framework.add_host(host):
                                    self.newQ.put(host)
                                self.foundQ.put(host)
                # break out of the loop
                attempt = self.max_attempts
            

class Module(framework.Framework):

    def __init__(self, params):
        framework.Framework.__init__(self, params)
        self.register_option('domain', self.global_options['domain'], 'yes', self.global_options['domain'])
        self.register_option('wordlist', './data/hostnames.txt', 'yes', 'path to hostname wordlist')
        self.register_option('nameserver', '8.8.8.8', 'yes', 'ip address of a valid nameserver')
        self.register_option('attempts', 3, 'yes', 'Number of retry attempts per host')
        self.register_option('threads', 1, 'yes', 'Number of threads')
        self.info = {
                     'Name': 'DNS Hostname Brute Forcer',
                     'Author': 'Tim Tomes (@LaNMaSteR53), Zach Grace (@ztgrace)',
                     'Description': 'Brute forces host names using DNS and updates the \'hosts\' table of the database with the results.',
                     'Comments': []
                     }

    def module_run(self):
        domain = self.options['domain']
        wordlist = self.options['wordlist']
        max_attempts = self.options['attempts']
        resolver = dns.resolver.get_default_resolver()
        resolver.nameservers = [self.options['nameserver']]
        resolver.lifetime = 3
        resolver.timeout = 2
        fake_host = 'sudhfydgssjdue.%s' % (domain)
        wordQ = Queue.Queue()
        foundQ = Queue.Queue()
        newQ = Queue.Queue()

        try:
            answers = resolver.query(fake_host)
            self.output('Wildcard DNS entry found. Cannot brute force hostnames.')
            return
        except (dns.resolver.NoNameservers, dns.resolver.Timeout):
            self.error('Invalid nameserver.')
            return
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            self.verbose('No Wildcard DNS entry found. Attempting to brute force DNS records.')
            pass

        # Load the wordlist into the queue
        if os.path.exists(wordlist):
            words = open(wordlist).read().split()
            for word in words:
                wordQ.put(word)

            # Start up the threads
            threads = []
            for i in range(self.options['threads']):
                t = DNSBrute(self, wordQ, foundQ, newQ, domain, resolver, max_attempts)
                threads.append(t)
                t.setDaemon(True)
                t.start()

            # Monitor for a keyboard interupt
            try:
                while wordQ.qsize() > 0:
                    for t in threads:
                        if t is not None and t.isAlive():
                            t.join(1)
            except KeyboardInterrupt:
                print "Caught Ctrl+C, exiting"
                for t in threads:
                    t.kill = True

                # empty out the word queue so the module will exit
                while not wordQ.empty():
                    wordQ.get()
                    wordQ.task_done()

            self.output('%d total hosts found.' % (foundQ.qsize()))
            if newQ.qsize() > 0: self.alert('%d NEW hosts found!' % (newQ.qsize()))
        else:
            self.error('Wordlist file not found.')
