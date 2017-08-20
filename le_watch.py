
import os
from subprocess import check_call
import sys

ENVIRONMENT_VARIABLES = [
    "webroot",
    "email",
    "subdomains",
    "domain",
    "subdomains_only"
]

ENV = {}
for varname in ENVIRONMENT_VARIABLES:
    ENV[varname] = os.environ.get(varname.upper())



def get_certs_for_domains(subdomains):
    domain = ENV['domain']
    email = ENV['email']
    webroot = ENV['webroot']
    domains = []

    only_subdomains = ENV['subdomains_only']

    if only_subdomains and only_subdomains != "true":
        domains.append(domain)

    for subdomain in subdomains:
        domains.append(subdomain + "." + domain)
    cmd = "letsencrypt certonly --webroot --agree-tos -m{email} -w{webroot}".format(
            email  =email,
            webroot=webroot
    )
    for domain in domains:
        cmd += " -d " + domain
        check_call(cmd, shell=True, stdout=sys.stdout)



if __name__ == "__main__":

    # make sure these environment variables are set
    for var in ["webroot", "email", "subdomains", "domain"]:
        if var not in ENV or not ENV[var]:
            print("Missing environment variable: {}".format(var.upper()))
            exit(1)

    # split subdomains on comma and pass
    get_certs_for_domains(ENV['subdomains'].split(","))

