import unittest

from address_book import Phone, Field, Record, AddressBook


class PhoneTest(unittest.TestCase):
    def test_valid_phone_number(self):
        self.assertTrue(Phone._validate_number("1234567890"))

    def test_invalid_phone_number_short(self):
        self.assertFalse(Phone._validate_number("12345"))

    def test_invalid_phone_number_long(self):
        self.assertFalse(Phone._validate_number("123456789012"))

    def test_invalid_phone_number_non_numeric(self):
        self.assertFalse(Phone._validate_number("12345abcde"))

    def test_invalid_phone_number_with_spaces(self):
        self.assertFalse(Phone._validate_number("123 456 7890"))

    def test_invalid_phone_number_with_special_characters(self):
        self.assertFalse(Phone._validate_number("123-456-7890"))


class TestField(unittest.TestCase):
    def test_initialization(self):
        value = "TestValue"
        field = Field(value)
        self.assertEqual(field.value, value)

    def test_string_representation(self):
        value = "TestValue"
        field = Field(value)
        self.assertEqual(str(field), value)

    def test_string_representation_with_integer(self):
        value = 12345
        field = Field(value)
        self.assertEqual(str(field), str(value))


class TestRecord(unittest.TestCase):
    def test_initialization(self):
        record = Record("John Doe")
        self.assertEqual(record.name.value, "John Doe")
        self.assertEqual(record.phones, [])

    def test_add_phone(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        self.assertEqual(len(record.phones), 1)
        self.assertEqual(record.phones[0].value, "1234567890")

    def test_remove_phone(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.remove_phone("1234567890")
        self.assertEqual(len(record.phones), 0)

    def test_remove_phone_not_found(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.remove_phone("0987654321")
        self.assertEqual(len(record.phones), 1)

    def test_edit_phone(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.edit_phone("1234567890", "0987654321")
        self.assertEqual(len(record.phones), 1)
        self.assertEqual(record.phones[0].value, "0987654321")

    def test_edit_phone_not_found(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.edit_phone("1111111111", "0987654321")
        self.assertEqual(record.phones[0].value, "1234567890")

    def test_find_phone(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        found = record.find_phone("1234567890")
        self.assertEqual(found, "1234567890")

    def test_find_phone_not_found(self):
        record = Record("John Doe")
        found = record.find_phone("1234567890")
        self.assertIsNone(found)

    def test_str_representation(self):
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        expected_str = "Contact name: John Doe, phones: 1234567890; 0987654321"
        self.assertEqual(str(record), expected_str)


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()

    def test_add_record(self):
        record = Record("John")
        self.address_book.add_record(record)
        self.assertEqual(len(self.address_book.data), 1)
        self.assertEqual(self.address_book.data["John"], record)

    def test_find_existing_record(self):
        record = Record("John")
        self.address_book.add_record(record)
        found_record = self.address_book.find("John")
        self.assertEqual(found_record, record)

    def test_find_non_existing_record(self):
        found_record = self.address_book.find("Jane")
        self.assertIsNone(found_record)

    def test_delete_existing_record(self):
        record = Record("John")
        self.address_book.add_record(record)
        self.address_book.delete("John")
        self.assertNotIn("John", self.address_book.data)

    def test_delete_non_existing_record(self):
        self.address_book.delete("Jane")
        self.assertNotIn("Jane", self.address_book.data)


if __name__ == "__main__":
    unittest.main()
