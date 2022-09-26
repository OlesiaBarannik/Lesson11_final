import json


def open_phonebook():
    with open("phonebook.json", "r+") as phonebook_file:
        try:
            phonebook = phonebook_file.read()
            phonebook = json.loads(phonebook)
        except json.JSONDecodeError:
            phonebook = {}

    return phonebook


def correct_input(valid_func, prompt: str, hint=False):
    valid = False

    if hint:
        print(hint)

    while not valid:
        value = input(prompt)
        valid = valid_func(value)

    return value


def add_new_entry():
    phone_number = "+380" + correct_input(valid_phone_number, "Enter your phone number: +380-",
                                          "Enter your phone number in next format: +380-XX-XXX-XX-XX. Country code by default +380 (Ukraine)")

    first_name = correct_input(valid_first_or_last_name, "Enter your name: ",
                               "Name should be less than 50 characters and contains only letters").lower().title()

    last_name = correct_input(valid_first_or_last_name, "Enter your last name: ",
                              "Last name should be less than 50 characters and contains only letters").lower().title()

    full_name = first_name + " " + last_name

    state = correct_input(valid_city_or_state, "Enter your state: ").strip()
    city = correct_input(valid_city_or_state, "Enter your city: ").strip()

    phonebook[phone_number] = {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "address": {
            "state": state,
            "city": city
        },
    }

    with open("phonebook.json", "w") as phonebook_file:
        json.dump(phonebook, phonebook_file, indent=4)


def search_by(key: str, searching_for: str):
    search_result = []

    if key == "phone_number":
        if phonebook.get(searching_for):
            search_result.append(searching_for)
        return search_result

    for phone_number in phonebook.keys():
        if key in ["state", "city"]:
            if phonebook[phone_number]["address"][key] == searching_for:
                search_result.append(phone_number)

        elif phonebook[phone_number][key] == searching_for:
            search_result.append(phone_number)

    return search_result



def delete_phone_number(phone_number: str, phonebook: dict):
    try:
        del phonebook[phone_number]
        print(f"Contact with phone number {phone_number} deleted.")
    except KeyError:
        print("Phone number is not exists!")

    with open("phonebook.json", "w") as phonebook_file:
        json.dump(phonebook, phonebook_file, indent=4)


def update_contact_info(phone_number: str, key: str, phonebook: str):
    try:
        phonebook[phone_number]

    except KeyError:
        print("Phone number is not exists!")

    if key == "phone_number":
        pass

    if key in ["state", "city"]:
        new_value = correct_input(valid_city_or_state, f"Enter your {key}: ").strip()
        phonebook[phone_number]["address"][key] = new_value

    if key in ["first_name", "last_name"]:
        new_value = correct_input(valid_first_or_last_name, f"Enter your {key.replace('_', ' ')}: ",
                                  "Name should be less than 50 characters and contains only letters").lower().title()
        phonebook[phone_number][key] = new_value

        phonebook[phone_number]["full_name"] = phonebook[phone_number]["first_name"] + " " + phonebook[phone_number]["last_name"]

    if key == "full_name":
        new_first_name = correct_input(valid_first_or_last_name, f"Enter your first name: ",
                                       "Name should be less than 50 characters and contains only letters").lower().title()

        new_last_name = correct_input(valid_first_or_last_name, f"Enter your last name: ",
                                      "Name should be less than 50 characters and contains only letters").lower().title()

        phonebook[phone_number]["first_name"] = new_first_name
        phonebook[phone_number]["last_name"] = new_last_name
        phonebook[phone_number]["full_name"] = contact["first_name"] + " " + contact["last_name"]

    with open("phonebook.json", "w") as phonebook_file:
        json.dump(phonebook, phonebook_file, indent=4)


def valid_phone_number(phone_number: str):
    phone_number = phone_number.split('-')  # ['96', '123', '40', '50']
    if len(phone_number) != 4:
        print("Not valid format!")
        return False

    format_of_elements = [2, 3, 2, 2]
    for index, digits in enumerate(phone_number):

        if not format_of_elements[index] == len(digits):
            print("Not valid format!")
            return False

        if not digits.isnumeric():
            print("Only digits can be in phone number!")
            return False

    return True


def valid_first_or_last_name(name: str):
    if len(name) > 50:
        return False
        print("Too many characters!")

    if not name.isalpha():
        print("Name must contains only alphabet letters!")
        return False

    return True


def valid_city_or_state(place_name: str):
    set_of_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- "

    if "  " in place_name:
        print("Too many spaces!")
        return False

    if len(place_name) > 50:
        print("Too many characters!")
        return False

    if (place_name[0] == "-") or (place_name[-1] == "-"):
        print("- can not be in the first place")
        return False

    for letter in place_name:
        if letter not in set_of_characters:
            print("Should only contain alphabet or -")
            return False

    return True

def exit_from_phonebook():
    print("Thank you!")
    exit()


def print_phonebook(phonebook: dict, key: list):
    for i in key:
        print(i, phonebook[i])




def print_menu():
    print("1. Add new entry")
    print("2. Search by phone number")
    print("3. Search by first name")
    print("4. Search by last name")
    print("5. Search by state")
    print("6. Search by city")
    print("7. Update contact info")
    print("8. Delete phone number")
    print("9. Exit")


menu_func = {1: add_new_entry, 2: search_by, 3: search_by, 4: search_by, 5:search_by, 6:search_by,
             7:update_contact_info, 8:delete_phone_number, 9: exit_from_phonebook}



def menu():
    print_menu()
    menu_choice = int(input("Input menu namber please: "))
    while not (1 <= menu_choice <= 9):
        print("There are no such menu choice!\n")
        print_menu()
        menu_choice = int(input("Input correct menu namber please: "))
    else:
        if menu_choice == 1:
            menu_func[menu_choice]()
        elif menu_choice == 2:
            result = menu_func[menu_choice]("phone_number", input("Please input searching phone number: "))
            print_phonebook(phonebook, result)
        elif menu_choice == 3:
            result = menu_func[menu_choice]("first_name", input("Please input searching first name: "))
            print_phonebook(phonebook, result)
        elif menu_choice == 9:
            menu_func[menu_choice]()
        elif menu_choice == 4:
            result = menu_func[menu_choice]("last_name", input("Please input searching last name: "))
            print_phonebook(phonebook, result)
        elif menu_choice == 5:
            result = menu_func[menu_choice]("state", input("Please input searching state: "))
            print_phonebook(phonebook, result)
        elif menu_choice == 6:
            result = menu_func[menu_choice]("city", input("Please input searching city: "))
            print_phonebook(phonebook, result)
        elif menu_choice == 7:
            menu_func[menu_choice] = update_contact_info(input("Please input phone_number: "), input("Please input update info: "
            "first_name, last_name, full_name, address: state city: "), phonebook)
        elif menu_choice == 8:
            menu_func[menu_choice] = delete_phone_number(input("Please input phone_number: "), phonebook)


phonebook = open_phonebook()

while True:
    menu()