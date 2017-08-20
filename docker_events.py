from docker import Client
import json
import utils
from constants import EMAIL, WEBROOT

client = Client(base_url='unix://var/run/docker.sock')
events = client.events(decode=True)




for event in events:
    print(event['Action'])
    if event['Action'] != 'start':
        continue

    container_id = event['id']
    container_attributes = client.inspect_container(container_id)
    env_list = container_attributes["Config"]['Env']
    environment = {}
    for var in env_list:
        parts = var.split("=")
        environment[parts[0]] = parts[1]

    if "SUBDOMAIN" in environment:
        subdomain = environment['SUBDOMAIN']
        port = environment.get('PORT') or "80"
        ip = container_attributes['NetworkSettings']['IPAddress']
        print(subdomain, ip, port)
        if utils.get_cert(subdomain, EMAIL):
            utils.move_cert(subdomain)
        else:
            print("Cert already exists")

        utils.write_site_config(subdomain, ip, port)