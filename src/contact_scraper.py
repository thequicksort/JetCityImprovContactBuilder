# For parsing and scraping HTML.
from bs4 import BeautifulSoup
from html_utils import email_from_raw_contact, is_email, is_real_contact, \
            phonenumber_from_raw_contact, remove_whitespace
from contact import Contact

################################################################################
# Hi gang,
#
# Jessica here.
#
# One day I'll be dead (or just gone in general). Even when that happens, you
# can still use this tool to update the contacts on your phones with new cast/crew
# members.
# :)
################################################################################

ORG_NAME = "Jet City Improv"

def parse_vcard_from_html(html_doc):
    """Parses the vcard info from the Fortress HTML doc.
    We rely on a handful of assumptions about the page layout to extract
    information.

    ASSUMPTIONS:

    - Each section of cast/crew/office type is separated by an <h3> tag
        - The content of this tag describes the role of its sibling items
        - e.g. <h3><span style="color: #800080;">Cast Section</span></h3>\n
            - Everything that follows this h3 tag will be cast members,
              until the next subsequent h3 tag is hit.
    - Each individual cast/crew/office member is designated with a <p> tag.
        - The name in enclosed in a <strong> tag. Their email and phone number are somewhere in the original tag.
        - e.g. <p><strong>Firstname LASTNAME&nbsp;</strong> email AT EMAIL.com&nbsp;&nbsp; /&nbsp;&nbsp; 555-555-5555</p>

    EDGE CASES:

    - Email and phone number are not always in the same order (e.g. sometimes email comes before phone)
    - Some individuals have their titles next to their names, separated with a comma.
    - Some indiviudlas have the word "(Former)" preceeding their names. I assume we want to leave these out of the final contact list.
    - For exactly one person (as of this writing), their phone number is enclosed in a second <p> tag. This is such an edge case that
      I've decided not to write code to handle it.

    Each cast member's info is nested within a <p> tag (to my knowledge
       that's the only delimiter). The name is enclosed in a <strong>
       tag.

       e.g.

       <p><strong>Firstname LASTNAME&nbsp;</strong> email AT EMAIL.com&nbsp;&nbsp; /&nbsp;&nbsp; 555-555-5555</p>


    Arguments:
        html_doc {string} -- The raw HTML page that contains the contact info.
    """

    # Initializes the parser
    soup = BeautifulSoup(html_doc, "html.parser")
    org = ORG_NAME

    # Finds the first section of cast/crew/office members.
    entry = soup.find("h3")
    vcards = ""
    while entry and (entry.name == "h3" or entry.name == "p"):
        if entry.name == "h3":
            heading = entry.text
        elif entry.name == "p" and is_real_contact(entry):
            title = heading
            entry = entry.find_next_sibling()
            contact = Contact(org=org)

            # First element: name in strong tag (sometimes the role is here as well)
            # Second element: email and phone number
            # e.g.
            # <p><strong>fred MEYER, Captain Director</strong> – (desk) x5&nbsp;&nbsp; /&nbsp;&nbsp; (cell) 555-555-5573&nbsp;&nbsp; /&nbsp;&nbsp; kwame AT example.org</p>
            raw_name = entry.contents[0]
            if len(entry.contents) < 2:
                entry = entry.find_next_sibling()
                continue
            raw_contact_info = entry.contents[1]
            name = remove_whitespace(raw_name.string)

            if len(name.split(",")) > 1:
                # For some entries, the name has a role following it, separated by a comma
                # Sometimes, multiple roles will be listed and also separate by a comma.
                # We limit the splits to 1 to get around the latter case.
                # e.g. "fred MEYER, Captain Director, Improvisor, and Father" will correctly split into
                # "fred MEYER" and "Captain Director, Improvisor, and Father", because it only split once.
                name, title = name.split(",", 1)
                title = remove_whitespace(title)
            contact.title = title

            if "(Former)" in name:
                # Skip people who are no longer involved with the theater.
                entry = entry.find_next_sibling()
                continue

            # Some people have their middle name listed (only one person at the time this was written)
            # To get around this, we split the name by spaces, then take the first and last entry.
            # Average case, this takes the first and last name if that's all that's listed
            # If a middle name is listed, we ignore it since it's in the middle.
            name_components = name.split(" ") # First and last name are separated by a space.
            given_name = name_components[0]
            family_name = name_components[-1]

            contact.full_name = name
            contact.given_name = given_name
            contact.family_name = family_name

            # Phone number and email are separated by a forward slash.
            # Which of the two comes first is not known a priori.
            # Plus, sometimes, the very first item is a desk extension. '
            # e.g.
            # <p><strong>kwame TURE, Production Director</strong> – (desk) x5&nbsp;&nbsp; /&nbsp;&nbsp; (cell) 555-555-5573&nbsp;&nbsp; /&nbsp;&nbsp; kwame AT example.org</p>
            # <p><strong>thomas SANKARA</strong>&nbsp; introvert AT gmail.com&nbsp;&nbsp; /&nbsp;&nbsp; 555-555-5597</p>
            #
            # Are both valid lines.
            #
            #
            # We start looking from the right-end of the split (i.e. negative indecies)
            # This means we can always ignore the desk extension.
            split_contact_info = remove_whitespace(raw_contact_info).split("/")
            if len(split_contact_info) < 2:
                entry = entry.find_next_sibling()
                continue
            first = split_contact_info[-2] # This is either a phone number, or an email address.
            second = split_contact_info[-1] # This is either an email address, or a phone number.

            email_raw = ""
            phone_number_raw = ""
            if is_email(first):
                email_raw = first
                phone_number_raw = second
            else:
                # First item was actually phone number, so swap them around.
                email_raw = second
                phone_number_raw = first

            phone_number = "" # Not everyone has a phone number.
            if len(split_contact_info) > 1:
                phone_number_raw = split_contact_info[1]
                phone_number = phonenumber_from_raw_contact(phone_number_raw)

            email = email_from_raw_contact(email_raw)

            contact.email = email
            contact.phone = phone_number

            # The contact is fully-formed. Now to make the vcard.

            vcard = contact.make_vcard()
            vcards += vcard

        entry = entry.find_next_sibling()
    return vcards
