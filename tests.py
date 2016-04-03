import unittest
from unittest import TestCase
from exceptions import FieldException
from regexen import (
    zip_re,
    first_last_name_re,
    last_first_name_re,    
    phone_re,
    ssn_re
)
from rolodex import Record


class RegexenTest(TestCase):
    def test_ssn1(self):
        test_str = "122 44 5678"
        m = ssn_re.match(test_str)
        self.assertTrue(m.group(0) == test_str)

    def test_ssn2(self):
        test_str = "000-11-6789"
        m = ssn_re.match(test_str)
        self.assertTrue(m.group(0) == test_str)

    def test_phone1(self):
        test_str = "(896)-391-7308"
        m = phone_re.match(test_str)
        self.assertTrue(m.group(0) == test_str)

    def test_phone2(self):
        test_str = "157 348 8325"
        m = phone_re.match(test_str)
        self.assertTrue(m.group(0) == test_str)

    def test_phone3(self):
        test_str = "555 11111 11111111"
        self.assertFalse(phone_re.match(test_str))

    def test_zip1(self):
        test_str = "123123121"
        self.assertFalse(zip_re.match(test_str))

    def test_zip2(self):
        test_str = "47185"
        m = zip_re.match(test_str)
        self.assertTrue(m.group(0) == test_str)

    def test_name1(self):
        test_str = "Noah, Moench"
        m = last_first_name_re.match(test_str)
        self.assertTrue(len(m.groups()) == 2)
        self.assertTrue(m.group(1) == "Noah")
        self.assertTrue(m.group(2) == "Moench")

    def test_name2(self):
        test_str = "Moench Noah"
        self.assertFalse(last_first_name_re.match(test_str))

    def test_name3(self):
        test_str = "Len Pollack"
        m = first_last_name_re.match(test_str)
        self.assertTrue(len(m.groups()) >= 2)
        self.assertTrue(m.group(1) == "Len")
        self.assertTrue(m.group(2) == "Pollack")

    def test_name4(self):
        test_str = "McGrath, Luke"
        m = last_first_name_re.match(test_str)
        self.assertTrue(len(m.groups()) == 2)
        self.assertTrue(m.group(2) == "Luke")
        self.assertTrue(m.group(1) == "McGrath")

    def test_line_split(self):
        test_str = "Dhillon, Beata, (843)-661-4252, 34-345-3456, 90022"
        fields = test_str.split(',')
        self.assertTrue(len(fields) == 5)

    def test_line_split2(self):
        test_str = "Margarete Stickle, 999 99 9999, 92493, 805 612 0845"
        fields = test_str.split(',')
        self.assertTrue(len(fields) == 4)


class RecordTest(TestCase):
    def setUp(self):
        self.record = Record()

    def tearDown(self):
        self.record = None

    def test_zip(self):
        test_str = "Shanika, Dodd, 82733, 940 761 0886, 111-22-3333"
        fields = test_str.split(',')
        self.assertTrue(len(fields) == 5)
        self.record.zipcode = "82733"
        self.assertEqual(self.record.zipcode, "82733")

    def test_zip2(self):
        with self.assertRaises(FieldException):
            self.record.zipcode = "Abcdefg"

    def test_phone1(self):
        test_str = "Leedy, Magan, (896)-391-7308, 888 88 8888, 48680"
        fields = test_str.split(',')
        self.assertTrue(len(fields) == 5)
        self.record.phone = "(896)-391-7308"
        self.assertEqual(self.record.phone, "(896)-391-7308")

    def test_phone2(self):
        with self.assertRaises(FieldException):
            self.record.phone = "(555)-11111-11111111"

    def test_ssn1(self):
        self.record.ssn = "222-33-4444"
        self.assertEqual(self.record.ssn, "222-33-4444")

    def test_ssn2(self):
        with self.assertRaises(FieldException):
            self.record.ssn = "96 tears"

    def test_name1(self):
        self.record.first_last = "Bernie Mallette"
        self.assertEqual(self.record.first_last, "Bernie Mallette")

    def test_name2(self):
        self.record.last_first = "Cadena, Clarinda"
        self.assertEqual(self.record.last_first, "Cadena, Clarinda")

    def test_name3(self):
        with self.assertRaises(FieldException):
            self.record.first_last = "Lee, Andrew"

    def test_name4(self):
        with self.assertRaises(FieldException):
            self.record.last_first = "Joe Smith"


class FieldTest(TestCase):
    def setUp(self):
        self.record = Record()

    def tearDown(self):
        self.record = None

    def test_last_first1(self):
        test_str = "Julian, Fanning, 82820, 555 11111 11111111, 222-33-4444"
        fields = test_str.split(',')
        self.record.last_first = ",".join(fields[0:2])
        self.assertEqual(self.record.last_first, "Julian, Fanning")

    def test_last_first2(self):
        test_str = "Bernie Mallette, 000-00-0000, 17300, 859 924 2843"
        fields = test_str.split(',')
        with self.assertRaises(FieldException):
            self.record.last_first = ",".join(fields[0:2])


class RolodexTest(TestCase):
    def setUp(self):
        self.record = Record()

    def tearDown(self):
        self.record = None

    def test_first_last1(self):
        test_str = "Englebert G. Humperdink, 123-45-6789, 36410, 839 014 8051"
        fields = test_str.split(',')
        if len(fields) == 5:
            if zip_re.match(fields[-1]):
                self.record.record_type = "last_zip"
            elif ssn_re.match(fields[-1]):
                self.record.record_type = "first_ssn"
        if len(fields) == 4:
            self.record.record_type = "first_phone"

        self.assertEqual(self.record.record_type, "first_phone")
        self.first_last_name = fields[0]
        self.ssn = fields[1]
        self.zipcode = fields[2]
        self.phone = fields[3]
        self.record.first_last = self.first_last_name
        self.record.ssn = self.ssn
        self.record.zipcode = self.zipcode
        self.record.phone = self.phone

        self.assertEqual(self.record.phone, "839 014 8051")
        self.assertEqual(self.record.first_last, "Englebert G. Humperdink")
        self.assertEqual(self.record.ssn, "123-45-6789")
        self.assertEqual(self.record.zipcode, "36410")

    def test_first_last2(self):
        test_str = "Annalee, Loftis, 97296, 905 329 2054, 123-45-6789"
        fields = test_str.split(",")
        self.first_last_name = "".join(fields[0:2])
        self.ssn = fields[4]
        self.zipcode = fields[2]
        self.phone = fields[3]
        self.record.first_last = self.first_last_name
        self.record.ssn = self.ssn
        self.record.zipcode = self.zipcode
        self.record.phone = self.phone

        self.assertEqual(self.record.phone, "905 329 2054")
        self.assertEqual(self.record.first_last, "Annalee Loftis")
        self.assertEqual(self.record.ssn, "123-45-6789")
        self.assertEqual(self.record.zipcode, "97296")


if __name__ == '__main__':
    unittest.main()
