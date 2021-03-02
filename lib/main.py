
# -*- coding: utf-8 -*-
# ^ For Python2 backwards compatibility
import os

# Q: Why not use Requests library for handling this HTTPS stuff? Seems like a no-brainer!
# A: Indeed! However, we're intentionally trying to keep this script free from external libraries,
#    even when they would make the code easier to read.
#
#    The reason for this is that fewer dependencies means an easier install on all cast member's setups.
#    (windows, mac, linux). Fewer system assumptions, etc. Just point a python version at it and go.

# For making network requests.
#import requests
import getpass
import json
import ssl

try:
    # Python 3
    from http.client import HTTPSConnection
except ImportError:
    # Python 2
    from httplib import HTTPSConnection

from contact_scraper import parse_vcard_from_html


def fetch_contact_page(password):
    """ Accesses

    Arguments:
        password {[string]} -- Password to enter Fortress. Be careful: NEVER hardcode or log this value.
    """

    contact_info_url = "www.jetcityimprov.org/fortress/phone-numbers-and-emails/"
    postpass_host = "www.jetcityimprov.org/wp-login.php?action=postpass"
    host = "www.jetcityimprov.org"
    body = { "body": { "post_password": getpass.getpass(), "Submit": "Enter" }}
    response_html = ""

    ssl_context = ssl.create_default_context() # To make sure we're connecting securely
    
    body_bytes = bytes(json.dumps(body), encoding='utf8')

    https = HTTPSConnection(host, context=ssl_context)
    https.connect()
    https.request("POST", "/wp-login.php?action=postpass", body=body_bytes)
    resp = https.getresponse()
    result = resp.read()
    response_html = bytes.decode(result, "utf-8")
    return response_html

def save_contacts(vcard, output_path, output_filename):
    """[summary]

    Arguments:
        vcard {[type]} -- [description]
        output_path {[type]} -- [description]
        output_filename {[type]} -- [description]
    """
    # First check that the file has an extension, and append one if it doesn't.
    filename, ext = os.path.splitext(output_filename)
    if not ext:
        filename += ".vcf"
    final_path = os.path.join(os.path.abspath(output_path), filename)
    with open(final_path, "w") as f:
        f.write(vcard)


if __name__ == "__main__":
    html_doc = fetch_contact_page("")
    vcard = parse_vcard_from_html(html_doc)
    save_contacts(vcard, ".", "my_friends")