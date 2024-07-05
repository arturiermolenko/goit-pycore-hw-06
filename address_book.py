import re
from collections import UserDict
from typing import Optional


class Field:
    """Base class for fields."""
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Name field."""
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    """Phone field with validation of number."""
    def __init__(self, number: str) -> None:
        if not self._validate_number(number):
            print("Invalid phone number format")
            return

        super().__init__(number)

    @staticmethod
    def _validate_number(number: str) -> bool:
        pattern = r"^\d{10}$"
        match = re.match(pattern=pattern, string=number)
        return match is not None


class Record:
    """Class for records."""
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        print("Record created")

    def add_phone(self, number: str) -> None:
        """Add a phone to the record"""
        phone = Phone(number)
        self.phones.append(phone)
        print(f"Added {phone}")

    def remove_phone(self, number: str) -> None:
        """Remove a phone from the record"""
        phone = self.find_phone_object(number)
        if phone:
            self.phones.remove(phone)
        else:
            print("Phone number not found")

    def edit_phone(self, old_number: str, new_number) -> None:
        """Edit a phone number in the record"""
        phone = self.find_phone_object(old_number)
        if phone:
            index = self.phones.index(phone)
            self.phones[index] = Phone(new_number)
        else:
            print("Phone number not found")

    def find_phone(self, number: str) -> str | None:
        """Find a phone number from the record"""
        phone = self.find_phone_object(number)
        if phone:
            return str(phone)
        print("Phone number not found")
        return None

    def find_phone_object(self, number: str):
        """Helper method to find a phone number from the record"""
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Address book class."""
    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record
        print(f"Record {record.name.value} added")

    def find(self, name: str) -> Optional[Record]:
        """Find a record in the address book."""
        if name in self.data:
            return self.data[name]
        print("Record not found")

    def delete(self, name: str) -> None:
        """Delete a record in the address book."""
        if name in self.data:
            self.data.pop(name)
        else:
            print("Record not found")


if __name__ == '__main__':
    # Creating a new address book
    book = AddressBook()

    # Creating a record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Adding John's record to the address book
    book.add_record(john_record)

    # Creating and adding a new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Printing all records in the book
    for name, record in book.data.items():
        print(record)

    # Finding and editing the phone number for John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

    # Finding a specific phone number in John's record
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Output: 5555555555

    # Deleting Jane's record
    book.delete("Jane")

    # Printing all records in the book
    for name, record in book.data.items():
        print(record)
