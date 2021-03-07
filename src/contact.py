# For creating the contact card.
import vobject

class Contact(object):
    """Contact represents the contact information for an individual that can be
       serialized into a vcard.
    """

    def __init__(self, family_name=None, given_name=None, full_name=None, org=None, title=None, email=None, phone=None):
        self.family_name = family_name
        self.given_name = given_name
        self.full_name = full_name
        self.org = org
        self.title = title
        self.email = email
        self.phone = phone

    def __str__(self):
        string_contact = "{full}, {role}. {title}. {email}\t{phone}".format(full=self.full_name,
                                                            role=self.role,
                                                            title=self.title,
                                                            email=self.email,
                                                            phone=self.phone)
        return string_contact

    def make_vcard(self):
        """Creates a formatted vcard string representing the contact.
        This can be appended to other vcards to make a comprehensive
        list of contacts.
        """
        contact_info = vobject.vCard()

        # Adds the contact's name.
        contact_info.add("n")
        contact_info.n.value = vobject.vcard.Name(family=self.family_name, given=self.given_name)
        contact_info.add("fn")
        contact_info.fn.value = self.full_name

        # Adds the contact's email.
        contact_info.add("email")
        contact_info.email.value = self.email
        contact_info.email.type_param = "INTERNET"

        # Adds the contact's phone number. Only cell is supported for now.
        if self.phone:
            contact_info.add("tel")
            contact_info.tel.type_param = "cell"
            contact_info.tel.value = self.phone

        # Adds the contact's role (e.g. House Manager), if one was given.
        if self.org:
            contact_info.add("org")
            contact_info.org.type_param = "ORG"
            contact_info.org.value = [self.org]

        # Adds the contact's title (e.g. Jet City Improv), if one was given.
        if self.title:
            contact_info.add("title")
            contact_info.title.type_param = "TITLE"
            contact_info.title.value = self.title

        # Serialize the contact info in the standard VCARD format.
        info = contact_info.serialize()
        return info
