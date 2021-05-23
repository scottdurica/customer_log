import unittest
import validate

class TestValidate(unittest.TestCase):

    def test_empty_str(self):
        self.assertFalse(validate.empty_str('1', 1))
        self.assertTrue(validate.empty_str('d', 2))
        self.assertFalse(validate.empty_str('1', 1))
        self.assertFalse(validate.empty_str('1', 1))

    def test_v_email(self):
        # regex_email = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        # regex_email = '^(\w|\.|\_|\-)+ -{0}+ [@](\w|\_|\-|\.)+[.]\w{2,3}$'

        # self.assertFalse(validate.v_email('abc-@mail.com'))
        # self.assertFalse(validate.v_email('abc..def@mail.com'))
        # self.assertFalse(validate.v_email('.abc@mail.com'))
        # self.assertFalse(validate.v_email('abc#def@mail.com'))
        # self.assertFalse(validate.v_email('abc.def@mail.c'))
        # self.assertFalse(validate.v_email('abc.def@mail#archive.com'))
        # self.assertFalse(validate.v_email('abc.def@mail'))
        # self.assertFalse(validate.v_email('abc.def@mail..com'))
        self.assertTrue(validate.v_email('abc-d@mail.com'))
        self.assertTrue(validate.v_email('abc.def@mail.com'))
        self.assertTrue(validate.v_email('abc@mail.com'))
        self.assertTrue(validate.v_email('abc_def@mail.com'))
        self.assertTrue(validate.v_email('abc.def@mail.cc'))
        self.assertTrue(validate.v_email('abc.def@mail-archive.com'))
        self.assertTrue(validate.v_email('abc.def@mail.org'))
        self.assertTrue(validate.v_email('abc.def@mail.com'))




if __name__ == '__main__':
    unittest.main()
