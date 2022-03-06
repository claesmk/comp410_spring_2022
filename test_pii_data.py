import unittest
from pii_data import read_data
from pii_data import Pii


class DataTestCases(unittest.TestCase):
    def test_read_data(self):
        expected_data = ['Aggie Pride Worldwide',
                         'Aggies Do', 
                         'Go Aggies',
                         'Aggie Strong!',
                         'Go Aggies',
                         'And Thats on 1891',
                         "Let's Go Aggies",
                         'Never Ever Underestimate an Aggie',
                         'Every Day The Aggie Way',
                         'Can I get an Aggie Pride',
                         'Aggies Do ^2',
                         'Aggie Pride For The Culture',
                         'We Are Aggies! We Are Proud!',
                         'Set My Future Self Up for Success!',
                         'AGGIE PRIDE!',
                         'We are Aggies',
                         'A-G-G-I-E, WHAT? P-R-I-D-E',
                         'Aggie Pride',
                         'Leaders Can Aggies Do',
                         'Mens et Manus',
                         'Aggies Aggies Aggies',
                         'Aggie Pride',
                         'Aggies are always number 1!',
                         'Because thats what Aggies do',
                         'Aggie Bred',
                         'Move forward with purpose',
                         'GO Aggie!',
                         'Aggie Pride']

        data = read_data('sample_data.txt')

        self.assertEqual(data, expected_data)

    def test_has_us_phone(self):
        # Test a valid US phone number
        test_data = Pii('My phone number is 970-555-1212')
        self.assertTrue(test_data.has_us_phone())

        # Test a partial US phone number
        test_data = Pii('My number is 555-1212')
        self.assertFalse(test_data.has_us_phone())

        # Test a phone number with incorrect delimiters
        test_data = Pii('My phone number is 970.555.1212')
        self.assertTrue(test_data.has_us_phone())

        # Test an invalid phone number
        test_data = Pii('My phone number is 970555.1212')
        self.assertFalse(test_data.has_us_phone())

    def test_has_us_phone_anonymize(self):
        # Anonymize a valid us phone number
        self.assertEqual(Pii('My phone number is 970-555-1212').has_us_phone(anonymize=True),
                         'My phone number is [us phone]')

        # Try an invalid one
        # Anonymize a valid us phone number
        self.assertEqual(Pii('My phone number is 970555-1212').has_us_phone(anonymize=True),
                         'My phone number is 970555-1212')

    def test_has_email(self):
        test_data = Pii('My email is kavondean@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kavon.dean@gmail.com')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kxdean@aggies.ncat.edu')
        self.assertEqual(test_data.has_email(), True)

        test_data = Pii('My email is kavondean.com')
        self.assertFalse(test_data.has_email())

        test_data = Pii('My email is kavondeangmail.com')
        self.assertFalse(test_data.has_email())

    def test_has_email_anonymize(self):
        self.assertEqual(Pii('My email is kavondean@gmail.com').has_email(anonymize=True),
                         'My email is [email]')

        self.assertEqual(Pii('My email is kavon.dean@gmail.com').has_email(anonymize=True),
                         'My email is [email]')

        self.assertEqual(Pii('My email is kxdean@aggies.ncat.edu.').has_email(anonymize=True),
                         'My email is [email].')

        self.assertEqual(Pii('My email is kavondean.com').has_email(anonymize=True),
                         'My email is kavondean.com')

        self.assertEqual(Pii('My email is kavondeangmail.com').has_email(anonymize=True),
                         'My email is kavondeangmail.com')

    def test_has_ipv4(self):
        test_data = Pii('My IP is 99.48.227.227')
        self.assertEqual(test_data.has_ipv4(), True)

        test_data = Pii('My IP is 192.168.1.1')
        self.assertEqual(test_data.has_ipv4(), True)

        # Test a partial ipv4
        test_data = Pii('My IP is 87.43.552')
        self.assertEqual(test_data.has_ipv4(), False)

        test_data = Pii('My IP is 192.343.2')
        self.assertEqual(test_data.has_ipv4(), False)

        # Test an ipv4 with incorrect delimiters
        test_data = Pii('My IP is 99-48-227-227')
        self.assertEqual(test_data.has_ipv4(), False)

        test_data = Pii('My IP is 192-433-1-1')
        self.assertEqual(test_data.has_ipv4(), False)

    def test_has_ipv4_anonymize(self):
        self.assertEqual(Pii('My ip is 192.168.1.1.').has_ipv4(anonymize=True),
                         'My ip is [IPv4].')

    def test_has_ipv6(self):
        # valid address
        test_data = Pii('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertTrue(test_data.has_ipv6())
        # invalid - not enough segments
        test_data = Pii('2001:0db8:0001:0000:0000:0ab9:C0A8')
        self.assertFalse(test_data.has_ipv6())
        # invalid - too many colons
        test_data = Pii('2001:0db8:0001:0000:0000:0ab9:C0A8:0102:')
        self.assertTrue(test_data.has_ipv6())
        # invalid - seperated by commas not colons
        test_data = Pii('2001,0db8,0001,0000,0000,0ab9,C0A8,0102')
        self.assertFalse(test_data.has_ipv6())

    def test_has_ipv6_anonymize(self):
        self.assertEqual(Pii('My ip address is 2001:0db8:85a3:0000:0000:8a2e:0370:7334').has_ipv6(anonymize=True),
                         'My ip address is [IPv6]')

    def test_has_name(self):
        #Test case for valid name
        test_data = Pii('Sean Tisdale')
        self.assertEqual(test_data.has_name(), True)

        #Test case for invalid name with number
        test_data = Pii('S3an Tisdale')
        self.assertEqual(test_data.has_name(), False)

         #Test case for invalid first name only
        test_data = Pii('Sean ')
        self.assertEqual(test_data.has_name(), False)


    def test_has_street_address(self):
        test_data = Pii('123 Addy Rd')
        self.assertEqual(test_data.has_street_address(), True)

        test_data = Pii('12356 Michellen Rd')
        self.assertEqual(test_data.has_street_address(), False)
         
        test_data = Pii('123 pope Blvd')
        self.assertEqual(test_data.has_street_address(), False)

        test_data = Pii('123 Rich Blvd')
        self.assertEqual(test_data.has_street_address(), True)

    def test_has_credit_card(self):
        test_data = Pii('My card is 1234-1234-1234-1234')
        self.assertTrue(test_data.has_credit_card())
        # invalid card
        test_data = Pii('My card is 123456-123456-1234-1234')
        self.assertFalse(test_data.has_credit_card())

    def test_has_at_handle(self):
        test_data = Pii('My handle is @joe_smith')
        self.assertTrue(test_data.has_at_handle())

        test_data = Pii('My email is joe@jon.com')
        self.assertFalse(test_data.has_at_handle())

    def test_has_pii(self):
        test_data = Pii()
        self.assertEqual(test_data.has_pii(), False)


if __name__ == '__main__':
    unittest.main()
