# For formatting unicode strings.
import unicodedata

def is_real_contact(p):
    """Returns true if this <p> element is an actual contact,
        and not a blank <p>. False otherwise.
    Arguments:
        p {bs4.element.Tag} -- <p> element to inspect

    Returns:
        [bool] -- Whether this element represents a contact.
    """
    return p.strong is not None

def remove_whitespace(u_string):
    """Removes unicode whitespace from a string.

    Arguments:
        string {string} -- String to remove any whitespace from.
    """
    stripped = unicodedata.normalize("NFKC", u_string).strip()
    return stripped

def is_email(raw):
    """Returns true if the raw string represents an "AT"-separated email
    address.

    Arguments:
        raw {str} -- A raw string.

    Returns:
        [bool] -- [description]
    """
    is_it_an_email = "AT" in raw
    return is_it_an_email

def email_from_raw_contact(raw_email_string):
    """Parses the email from raw string. The raw string can contain whitespaces
    and unicode white space.

    Arguments:
        raw_email_string {str} -- String that takes the form "EMAIL AT ADDRESS.COM"

    Returns:
        str -- Email string in the form "EMAIL@ADDRESS.COM"
    """
    email_components = list(map(lambda x: x.strip(), remove_whitespace(raw_email_string).split("AT")))
    email = "@".join(email_components)
    return email

def phonenumber_from_raw_contact(raw_phone_string):
    """Parses a phone number from a raw contact string, which could include
    unicode whitespaces.
    e.g. "&nbsp;&nbsp;&nbsp; /&nbsp;&nbsp; 555-555-1959"

    Arguments:
        raw_phone_string {str} -- Raw unicode string that includes a phone number.
         e.g. "&nbsp;&nbsp;&nbsp; /&nbsp;&nbsp; 555-555-1959"

    Returns:
        [str] -- Phone number as a string.
    """
    phonenumber = unicodedata.normalize("NFKC", raw_phone_string).strip()
    # Some phone numbers are prefixed with "(cell)", get rid of that
    phonenumber = phonenumber.strip("(cell)") \
                                .strip(" – ")
    return phonenumber
