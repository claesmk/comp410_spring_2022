import re


# PII = Personally Identifiable Information
# Create a new Pii class based on str
class Pii(str):
    # For help with regex see
    # https://regex101.com
    # https://www.w3schools.com/python/python_regex.asp
    def has_us_phone(self, anonymize=False):
        # https://docs.python.org/3.9/library/re.html?highlight=subn#re.subn
        newstr, count1 = re.subn(r'\d{9}', '[us phone]', self)

        # Match a US phone number ddd-ddd-dddd ie 123-456-7890
        newstr, count2 = re.subn(r'\d{3}[-.]\d{3}[-.]\d{4}', '[us phone]', newstr)

        if anonymize:
            # Since str is immutable it's better to stay with the spec and return a new
            # string rather than modifying self
            return newstr
        else:
            # Keep the original requirement in place by returning True or False if
            # a us phone number was present or not.
            return bool(count1+count2)

    def has_email(self, anonymize=False):
        newstr, count1 = re.subn(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9._%+-]+\w{3}', '[email]', self)
        if anonymize:
            return newstr
        return bool(count1)

    def has_ipv4(self, anonymize=False):
        newstr, count1 = re.subn(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', '[IPv4]', self)
        if anonymize:
            return newstr
        return bool(count1)

    def has_ipv6(self, anonymize=False):
        newstr, count1 = re.subn(r'(?:[0-9a-fA-F]{0,4}:){7}[0-9a-fA-F]{0,4}', '[IPv6]', self)
        if anonymize:
            return newstr
        return bool(count1)

    def has_name(self, anonymize=False):
        newstr, count1 = re.subn(r'[A-Z][a-z]+\s[A-Z][a-z]+', '[name', self)
        if anonymize:
            return newstr
        return bool(count1)

    def has_street_address(self):
        match = re.search(r'^\d{0,4}\s[A-Z][a-zA-Z]{2,30}\s\b(Ave|St|Blvd|Rd)\b', self)
        if match:
            return True
        return False

    def has_credit_card(self):
        match = re.search(r'\d{4}-\d{4}-\d{4}-\d{4}', self)
        if match:
            return True
        return False

    def has_at_handle(self):
        match = re.search(r'(^|\s)@\w+', self)
        if match:
            return True
        return False

    def has_pii(self):
        return self.has_us_phone() or self.has_email() or self.has_ipv4() or self.has_ipv6() or self.has_name() or \
               self.has_street_address() or self.has_credit_card() or self.has_at_handle()


def read_data(filename: str):
    data = []
    with open(filename) as f:
        # Read one line from the file stripping off the \n
        for line in f:
            data.append(line.rstrip())
    return data


if __name__ == '__main__':
    data = read_data('sample_data.txt')
    print(data)
    print('---')

    pii_data = Pii('My phone number is 123-123-1234')
    print(pii_data)
    
    pii_data = Pii('My IPv4 is 99.48.227.227')
    print(pii_data)

    if pii_data.has_pii():
        print('There is PII data preset')
    else:
        print('No PII data detected')
