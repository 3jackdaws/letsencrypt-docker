from constants import SITE_CONFIG_DIR, WEBROOT, KEY_OUTPUT_DIR
import os
import sys
from subprocess import check_call
import shutil

def generate_nginx_site_config(server_name,ip, port=80):
    return """
server{
    listen 443 ssl;
    server_name %s;
    
    ssl on;
    ssl_certificate         /config/keys/%s/fullchain1.pem;
    ssl_certificate_key     /config/keys/%s/privkey1.pem;
    
    location /{
        proxy_pass http://%s:%s;
    }
}
    """ % (server_name, server_name, server_name, ip, port)

def write_site_config(server_name, ip, port=80):
    filename = SITE_CONFIG_DIR + "/" + server_name + ".conf"
    if not os.path.isfile(filename):
        config = generate_nginx_site_config(server_name, ip, port)
        with open(filename) as fp:
            fp.write(config)
    else:
        print("Site config already exists.  Skipping.")



def get_cert(domain, email):
    cmd = "letsencrypt certonly --webroot --agree-tos -m{email} -w{webroot} -d{domain}".format(
        email=email,
        webroot=WEBROOT,
        domain=domain
    )
    try:
        check_call(cmd, shell=True, stdout=sys.stdout, timeout=10)
        return True
    except Exception as e:
        print(e)
        return False

def move_cert(domain):
    final_dir = KEY_OUTPUT_DIR + "/" + domain
    os.rmdir(final_dir)
    check_call("cp -R {} {}".format("/etc/letsencrypt/archive/" + domain, final_dir))







