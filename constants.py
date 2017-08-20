import os, sys

KEY_OUTPUT_DIR  = "/keys"

SITE_CONFIG_DIR = "/sites"

WEBROOT         = "/webroot"

EMAIL           = os.environ.get("EMAIL") or sys.exit("This container requires that the EMAIL environemtn variable is set.")