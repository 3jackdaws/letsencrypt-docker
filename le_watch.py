
import os
from subprocess import check_output

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

    if ENV['subdomains_only'].lower() is not "true":
        domains.append(domain)

    for subdomain in subdomains:
        domains.append(subdomain + "." + domain)

    for domain in domains:
        cmd = "letsencrypt certonly --dry-run --webroot --agree-tos -m{email} -w{webroot} -d {domain}".format(
            email  =email,
            webroot=webroot,
            domain =domain
        )
        check_output(cmd, shell=True)



if __name__ == "__main__":

    # make sure these environment variables are set
    for var in ["webroot", "email", "subdomains", "domain"]:
        if var not in ENV or not ENV[var]:
            print("Missing environment variable: {}".format(var.upper()))
            exit(1)

    # split subdomains on comma and pass
    get_certs_for_domains(ENV['subdomains'].split(","))

