import utils

mk = utils.generate_nginx_site_config("docker.isogen.net", "portainer", "9000")

print(mk)