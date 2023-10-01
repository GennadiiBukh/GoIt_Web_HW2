from collections import UserDict
from datetime import datetime
import pickle
from abc import ABC, abstractmethod

#Створюється базовий абстрактний клас Field, який буде включати загальну логіку для полів
class Field(ABC):
    def __init__(self, value=None):
        self.value = value

    @abstractmethod
    def value(self):
        pass
           
    @abstractmethod 
    def display_info(self):  #виводить інформацію про поле
        pass

#Створюються класи що успадковуються від Field
class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def value(self, value):
        if self.is_valid_phone(value):
            self._value = value
        else:
            raise ValueError(f"Неправильний формат телефона: {value}")

    def is_valid_phone(self, value):
        try:
            if len(value) == 12 and value.isdigit():
                return True
        except ValueError:
            return False

    def display_info(self):
        return f"{self.value}" if self.value else ""

class Name(Field):
    def __init__(self, value=None):
        super().__init__(value)
    
    def value(self, value):
        self._value = value

    def display_info(self):
        return f"{self.value}" if self.value else ""
    
class Email(Field):
    def __init__(self, value=None):
        super().__init__(value)
    
    def value(self, value):
        self._value = value

    def display_info(self):
        return f"{self.value}" if self.value else ""
    
class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def value(self, value):
        if self.is_valid_date(value):
            self._value = value
        else:
            raise ValueError(f"Неправильний формат дати: {value}")

    def is_valid_date(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False
    
    def display_info(self):
        return f"{self.value}" if self.value else ""
    
class Record:
    def __init__(self, name: Name, phones: list, emails: list, birthday=None):
        self.name = name
        self.phones = phones
        self.emails = emails
        self.birthday = birthday

    @abstractmethod
    def display_info(self):
        pass

class PersonRecord(Record):
    def __init__(self, name: Name, phones: list, emails: list, birthday=None):
        super().__init__(name, phones, emails, birthday)

    def display_info(self):
        phone_info = ", ".join(phone.display_info() for phone in self.phones)
        email_info = ", ".join(email.display_info() for email in self.emails)
        birthday_info = f"{self.birthday.display_info()}" if self.birthday else ""
        return f"Name: {self.name.display_info()}, Phones: {phone_info}, Emails: {email_info}, Birthday: {birthday_info}"

class RecordManager:
    def __init__(self, record: Record):
        self.record = record

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.record.phones:
            self.record.phones.append(phone_number)

    def add_email(self, email):
        email_adress = Email(email)
        if email_adress not in self.record.emails:
            self.record.emails.append(email_adress)

    def find_phone(self, value):
        pass

    def delete_phone(self, phone):
        if phone in self.record.phones:
            index = self.record.phones.index(phone)
            self.record.phones.remove(phone)
            return index
        else:
            return None

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.record.phones:
            index = self.record.phones.index(old_phone)
            self.record.phones[index] = new_phone
            return index
        else:
            return None

    def days_until_birthday(self):
        if self.birthday.value:
            today = datetime.today().date()
            birthday = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()

            next_birthday = birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            days_left = (next_birthday - today).days
            return days_left
        else:
            return None       
        
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)            
    
    def iterator(self, N):
        count = 0
        views = []        
        for record in self.data.values():
            views.append(PersonRecord.display_info(record))
            count += 1
            if count == N:
                yield "; ".join(views)
                count = 0
                views = []
        if views:
            yield "\n".join(views)

class FileManagerAndSearch:
    def __init__(self, address_book: AddressBook):
        self.address_book = address_book

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.address_book.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.address_book.data = pickle.load(file)
        except FileNotFoundError:
            print("Файл не зайдено")
        except Exception as error:
            print(f"Виникла помилка: {error}")

    def search(self, search_str: str):
        result = []
        for name, record in self.address_book.data.items():
            result.append(name) if search_str.lower() in name.lower() else None
            for email in record.emails:
                if name not in result:
                    result.append(name) if search_str.lower() in email.value.lower() else None
            for phone in record.phones:
                if name not in result:
                    result.append(name) if search_str in phone.value else None
        return result


if __name__ == '__main__':
    
    addressbook = AddressBook()
    
    def init_contact():
        rec = Record(name, all_phones, all_emails, birthday)
        addressbook.add_record(rec)
        return rec
    
    def print_contact(rec):        
        PersonRecord.display_info(rec)                       
        print("До дня народження:", RecordManager.days_until_birthday(rec), "днів")
        
    try:
        name = Name("Andrew")
        phone1 = Phone()
        phone1.value = "380671234455"
        phone2 = Phone()
        phone2.value = "380503216677"
        all_phones = [phone1, phone2]
        email = Email('andrew@gmail.com')
        all_emails = [email]
        birthday = Birthday()
        birthday.value = "18.08.2003"
        rec = init_contact()
                
        name = Name("Sergii")
        phone1 = Phone()
        phone1.value = "380673451270"
        phone2 = Phone()
        phone2.value = "380502321517"
        all_phones = [phone1, phone2]
        email = Email('sergii@gmail.com')
        all_emails = [email]
        birthday = Birthday()
        birthday.value = "21.07.1999"
        rec = init_contact()
        
        name = Name("Oleg")
        phone1 = Phone()
        phone1.value = "380938761535"
        phone2 = Phone()
        phone2.value = "380502329870"
        all_phones = [phone1, phone2]
        email = Email('oleg@gmail.com')
        all_emails = [email]
        birthday = Birthday()
        birthday.value = "17.02.2004"
        rec = init_contact()
        
        name = Name("Olga")
        phone1 = Phone()
        phone1.value = "380933458790"
        phone2 = Phone()
        phone2.value = "380507778899"
        all_phones = [phone1, phone2]
        email1 = Email('olga@gmail.com')
        email2 = Email('olga@yahoo.com')
        all_emails = [email1, email2]
        birthday = Birthday()
        # birthday.value = "16.03.2001"
        rec = init_contact()
        
        N=1 # Кількість записів для виводу за одну ітерацію
        
        for views in addressbook.iterator(N):
            print(views)

    except ValueError as error:
        print(error)

    # Збереження адресної книги у файл
    FileManagerAndSearch(addressbook).save_to_file('addressbook.pkl')

    # Відновлення адресної книги з файла
    loaded_addressbook = AddressBook()
    FileManagerAndSearch(loaded_addressbook).load_from_file('addressbook.pkl')

    # Перевірка відновленої з файла адресної книги
    print('\n')
    for name, record in loaded_addressbook.items():
        phones = [phone.value for phone in record.phones]
        emails = [email.value for email in record.emails]
        print(name, phones, emails, record.birthday.value if record.birthday else '')

    # Пошук в адресній книзі
    while True:
        print('\n')
        search_str = input('Введіть рядок для пошуку("Enter" для завершення) >> ')
        if search_str == '':
            break
        found = FileManagerAndSearch(loaded_addressbook).search(search_str)
        print(found) if found else print('Нікого не знайдено')
