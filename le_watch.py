import time
import os
from ruamel.yaml import round_trip_dump, round_trip_load
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from subprocess import check_output

CONFIG_FILE = "/config/config.yaml"

CONFIG_FILE = os.path.realpath(CONFIG_FILE)

CONFIG_TEXT = """
webroot: /var/www
status: ready
email: example@example.com
domains:
    - example.com
    - example2.com
"""

CONFIG = {}

def load_config():

    try:
        temp = round_trip_load(open(CONFIG_FILE))
        if "email" not in temp:
            raise
    except Exception as e:
        print(e)
        with open(CONFIG_FILE, "w+") as fp:
            fp.write(CONFIG_TEXT)
            fp.seek(0)
            temp = round_trip_load(fp)
    return temp

def reset_config_status():
    try:
        conf = load_config()
        conf['status'] = "updated"
        with open(CONFIG_FILE, "w+") as fp:
            round_trip_dump(conf, fp)
        return True
    except:
        return False


def get_certs_for_domains(domains):
    for domain in domains:
        cmd = "letsencrypt certonly --dry-run --webroot --agree-tos -m{email} -w{webroot} -d {domain}".format(
            email  =CONFIG['email'],
            webroot=CONFIG['webroot'],
            domain =domain
        )
        print(cmd)
        # check_output(cmd, shell=True)

def ready_to_update():
    try:
        status = round_trip_load(open(CONFIG_FILE))['status']
        return status.lower() == "ready"
    except Exception as e:
        print(e)
        return False


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        global CONFIG
        if isinstance(event, FileModifiedEvent):
            if CONFIG_FILE == os.path.realpath(event.src_path):
                if ready_to_update():
                    print("{} modified.".format(event.src_path))
                    previous_domains = set(CONFIG['domains'])
                    CONFIG = load_config()
                    new_domains = set(CONFIG['domains'])
                    different_domains = [d for d in new_domains if d not in previous_domains]
                    get_certs_for_domains(different_domains)
                    reset_config_status()


if __name__ == "__main__":
    CONFIG = load_config()
    get_certs_for_domains(CONFIG['domains'])
    reset_config_status()
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except:
        observer.stop()
        print("Error")

    observer.join()