
import os
# For making network requests.
import requests

from contact_scraper import parse_vcard_from_html

def fetch_contact_page(password):
    """ Accesses

    Arguments:
        password {[string]} -- Password to enter Fortress. Be careful: NEVER hardcode or log this value.
    """

    contact_info_url = "http://www.jetcityimprov.org/fortress/phone-numbers-and-emails/"
    postpass_url = "http://www.jetcityimprov.org/wp-login.php?action=postpass"
    body = { "post_password": password,
             "Submit": "Enter" }
    response_html = ""
    with requests.session() as session:
        # First, login with appropriate credentials to access the fortress page.
        session.post(postpass_url, data=body)
        # Now that we're logged in, fetch the contact page.
        response = session.get(contact_info_url)
        response_html = response.text
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