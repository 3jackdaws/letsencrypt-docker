import time
import os
from yaml import safe_dump, safe_load
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from subprocess import check_output

WATCH_FILE = "./config.yaml"
CONFIG_FILE = "./config.yaml"

WATCH_FILE = os.path.realpath(WATCH_FILE)

CONFIG_TEXT = """
email: example@example.com
webroot: /var/www
domains:
    - example.com
    - example2.com
"""

CONFIG = {}

def load_config():

    try:
        temp = safe_load(open(CONFIG_FILE))
        if "email" not in temp:
            raise
    except:
        with open(CONFIG_FILE, "w+") as fp:
            fp.write(CONFIG_TEXT)
            fp.seek(0)
            temp = safe_load(fp)
    return temp


def get_certs_for_domains(domains):
    for domain in domains:
        cmd = "letsencrypt certonly --dry-run --webroot --agree-tos -m{email} -w{webroot} -d {domain}".format(
            email  =CONFIG['email'],
            webroot=CONFIG['webroot'],
            domain =domain
        )
        check_output(cmd, shell=True)


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        global CONFIG
        if isinstance(event, FileModifiedEvent):
            if WATCH_FILE == os.path.realpath(event.src_path):
                print("{} modified.".format(event.src_path))
                previous_domains = set(CONFIG['domains'])
                CONFIG = load_config()
                new_domains = set(CONFIG['domains'])
                different_domains = [d for d in new_domains if d not in previous_domains]
                get_certs_for_domains(different_domains)


if __name__ == "__main__":
    CONFIG = load_config()
    get_certs_for_domains(CONFIG['domains'])
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