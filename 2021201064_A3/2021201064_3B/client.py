import requests
import random
import json
url = "http://127.0.0.1:8000/"


def show_menu():
    '''Sending request to server to get menu list to display'''
    menu_item = (requests.get(url + "menu_display")).json()
    print("\n----------------------------------Menu----------------------------------\n")
    print("---------------------------------------------------")
    print(f"|      Id       |   Half Plate   |   Full Plate   |")
    print("---------------------------------------------------")
    item_list = []
    for item in menu_item:
        print(
            f"|{item:^15}| {menu_item[item]['half']:<15}| {menu_item[item]['full']:<15}|")
        item_list.append([item,
                          menu_item[item]['half'],
                          menu_item[item]['full']])
    print("---------------------------------------------------")
    return item_list


def show():
    '''Taking input from User for username and password'''
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password


def register():
    '''Taking input from user and making request to server to
        add the user in database'''
    username, password = show()
    response = requests.post(
        url + "add_user",
        json={
            'username': username,
            'password': password})
    if int(response.content.decode('utf-8')) == 1:
        print("Register Successfuly Please login now")
    else:
        print("User name is already taken")


def login():
    '''Taking username & password make request from user
        make request to server to authenticate user'''
    username, password = show()
    response = requests.post(
        url + "login_user",
        json={
            'username': username,
            'password': password})
    if int(response.content.decode('utf-8')) in (1, 2):
        print("Login Successfully")
        return username, int(response.content.decode('utf-8'))
    else:
        print("wrong Username and Password")
        return "", 0


def input_from_user():
    '''Taking menu input from user in Item no   Plate type  Quantity formate
    user can enter any number of order and to exit they need to enter two times'''
    order_from_user_list = []
    while True:
        order_input_line = input()
        if order_input_line:
            order_from_user_list.append(order_input_line.split())
        else:
            break
    return order_from_user_list


def input_tip_from_user():
    '''Proving option to user to select tip and returing the tip percentage'''
    print("Please Add Tip percentage select the following options")
    print("1. 0%")
    print("2. 10%")
    print("3. 20%")
    tip_percentage_input = int(input())
    if(tip_percentage_input == 1):
        return 0
    if(tip_percentage_input == 2):
        return 10
    if(tip_percentage_input == 3):
        return 20


def calculate_total_price(item_list, order_from_user_list):
    '''After taking input from user we calculate the price for these item and store in list
    for each item after that we are checking if we same item id and plate type if yes then
    adding both to one and returning these value'''
    menu_result_list = []
    for item_from_user in order_from_user_list:
        temp_menu_result_list = []
        for item_from_menu in item_list:
            if(item_from_user[0] == item_from_menu[0]):
                if(item_from_user[1] == 'half'):
                    temp_menu_result_list.append(item_from_user[0])
                    temp_menu_result_list.append(item_from_user[1])
                    temp_menu_result_list.append(int(item_from_user[2]))
                    temp_menu_result_list.append(
                        float(item_from_user[2]) * float(item_from_menu[1]))
                else:
                    temp_menu_result_list.append(item_from_user[0])
                    temp_menu_result_list.append(item_from_user[1])
                    temp_menu_result_list.append(int(item_from_user[2]))
                    temp_menu_result_list.append(
                        float(item_from_user[2]) * float(item_from_menu[2]))
        menu_result_list.append(temp_menu_result_list)
    menu_result_list_size = len(menu_result_list)
    for menu_result_list_row_1 in range(0, menu_result_list_size):
        for menu_result_list_row_2 in range(
                menu_result_list_row_1 + 1,
                menu_result_list_size):
            if((menu_result_list[menu_result_list_row_1][0] == menu_result_list[menu_result_list_row_2][0]) and (menu_result_list[menu_result_list_row_1][1] == menu_result_list[menu_result_list_row_2][1])):
                menu_result_list[menu_result_list_row_1][2] = menu_result_list[menu_result_list_row_1][2] + \
                    menu_result_list[menu_result_list_row_2][2]
                menu_result_list[menu_result_list_row_1][3] = menu_result_list[menu_result_list_row_1][3] + \
                    menu_result_list[menu_result_list_row_2][3]
                menu_result_list[menu_result_list_row_2][0] = "-1"
    remove_not_required_result_list = []
    for menu_result_list_row in menu_result_list:
        if(menu_result_list_row[0] != "-1"):
            remove_not_required_result_list.append(menu_result_list_row)
    menu_result_list = remove_not_required_result_list
    return menu_result_list


def total_price_including_tip(menu_result_list, tip_percentage):
    '''Below function is called to calculate total value of items and final total value
    which include tip and return these two value'''
    total_value = 0
    for menu_result_list_row in menu_result_list:
        total_value = total_value + menu_result_list_row[3]
    return total_value, total_value + total_value * tip_percentage / 100


def display_pattern(discount):
    '''This function is called from test_your_luck_scheme if discount is certain value then
    it will print one of two pattern'''
    if(discount < 0):
        print(" ****            ****	")
        print("|    |          |    |   ")
        print("|    |          |    |   ")
        print("|    |          |    |   ")
        print(" ****	        ****    ")
        print("                         ")
        print("          {}             ")
        print("    ______________       ")
    else:
        print(" **** ")
        print("*    *")
        print("*    *")
        print("*    *")
        print("*    *")
        print(" **** ")
    print("\n\n")


def test_your_luck_scheme(total_price_with_tip):
    '''Calling this function from main to check if user is interested in test your luck scheme
    or not if not then we proceed with final value displayed if yes then we calculate
    chance of wining by genrating random number between 1 to 100 and if particular number
    fall in some category then it can be discount ot increase and print the dicount/increase
    value and call function to print pattern and return discount percentage'''
    print("Restaurant has ongoing Test your luck scheme uou want to participate(yes or No)?")
    choice_from_user = input()
    if choice_from_user in ("no", "n", "No", "n", "NO"):
        return 0
    lucy_number = random.randint(1, 100)
    discount = 0
    if lucy_number >= 1 and lucy_number <= 5:
        discount = -50
    if lucy_number >= 6 and lucy_number <= 15:
        discount = -25
    if lucy_number >= 16 and lucy_number <= 30:
        discount = -10
    if lucy_number >= 31 and lucy_number <= 50:
        discount = 0
    if lucy_number >= 51 and lucy_number <= 100:
        discount = 20
    print("\n--------------------------------------")
    print(
        "Discount Value/Increase Value\t",
        "{:.2f}".format(
            discount *
            total_price_with_tip /
            100))
    print("--------------------------------------\n\n")
    display_pattern(discount)
    return discount


def display_item_with_total_price(menu_result_list):
    '''Below function is called from main to display item id with their total price
    in item id[plat][quantity]: total value format'''
    item_list = []
    for menu_result_list_row in menu_result_list:
        string = "Item " + str(menu_result_list_row[0]) + " [" + str(menu_result_list_row[1]) + "] [" + str(
            menu_result_list_row[2]) + "]: " + str(menu_result_list_row[3])
        item_list.append([user_id,
                          menu_result_list_row[0],
                          menu_result_list_row[1],
                          menu_result_list_row[2],
                          menu_result_list_row[3]])
        print(string)
    item_list_json = {}
    item_list_json.update({"data": item_list})
    requests.post(url + "trans_detail", json=item_list_json)


def display_total_values(
        total_price,
        tip_percentage,
        discount_from_scheme,
        each_person_share,
        final_value):
    '''Displaying final value of item and total value including tip and discount'''
    print("Total:", "{:.2f}".format(total_price))
    print("Tip Percentage:" + str("{:.2f}".format(tip_percentage) + "%"))
    print("Discount/Increase:", "{:.2f}".format(discount_from_scheme))
    print("Final Total:", "{:.2f}".format(final_value))
    print("\n----------------------------------------")
    print("Share for each person is", "{:.2f}".format(each_person_share))
    print("----------------------------------------\n\n")


def billmain():
    '''this function is used to read data from database bill menu table and store menu
        in item list variable'''
    item_list = show_menu()
    '''After getting value from above function below function is used to
        display in tab sepearted format'''
    print("Please Enter your order info( Item no   Plate type  Quantity):\n")
    '''Taking input from usert in item id plate quatity format user can enter any number
        of order and enter two times to exit from menu ordering'''
    order_from_user_list = input_from_user()
    '''Taking user input for tip in form of option'''
    tip_percentage = input_tip_from_user()
    '''calling below function to calculate total price of each item '''
    menu_result_list = calculate_total_price(item_list, order_from_user_list)
    '''To get total price and price after including tip calling below function'''
    total_price, total_price_with_tip = total_price_including_tip(
        menu_result_list, tip_percentage)
    '''After getting total price including tip we are printing value to command promt'''
    print("\n--------------------------------------------------")
    print("Your total Amount for this order is",
          "{:.2f}".format(total_price_with_tip))
    print("--------------------------------------------------\n")
    print("Enter number of you want to split this bill")
    '''Taking input from user to get number of people to divide the bill'''
    people_to_split_bill = int(input())
    each_person_share = total_price_with_tip / people_to_split_bill
    '''Display each person share'''
    print("\n----------------------------------------")
    print("Share for each person is ", "{:.2f}".format(each_person_share))
    print("----------------------------------------\n\n")
    '''Asking user for if they want to part in test your luck scheme or not if yes then
        calculating probabilty to do that calling below function'''
    discount_from_scheme = test_your_luck_scheme(total_price_with_tip)
    '''Display value of each item id in seperat line '''
    display_item_with_total_price(menu_result_list)
    final_value = total_price_with_tip + \
        discount_from_scheme * total_price_with_tip / 100
    each_person_share = final_value / people_to_split_bill
    discount_from_scheme_value = total_price_with_tip * discount_from_scheme / 100
    '''Displaying total price excluding tip, tip percentage, discount/increase amount
        if they participated in scheme, final total price and updated share of each person'''
    display_total_values(
        total_price,
        tip_percentage,
        discount_from_scheme_value,
        each_person_share,
        final_value)
    final_value_list = []
    final_value_list.extend([user_id,
                             total_price,
                             tip_percentage,
                             discount_from_scheme_value,
                             each_person_share,
                             final_value])
    final_value_list_json = {}
    '''Enter data in database'''
    final_value_list_json.update({"data": final_value_list})
    requests.post(url + "trans", json=final_value_list_json)


def chef_menu_change():
    '''Taking input from chef for order and menu change and add data to data after
        making request to server'''
    print("Please enter new menu item in ( Item no   Half plate price  Full plate Price) format ")
    new_menu_items = input_from_user()
    new_menu_item_json = {}
    new_menu_item_json.update({"data": new_menu_items})
    requests.post(url + "add_new_menu_item", json=new_menu_item_json)
    print("Added Successfully")


def trans(username):
    '''Displaying transaction detail of each trasaction done by user or chef'''
    response = requests.post(url + "get_trans", json={'username': username})
    trans_item_json = json.loads(response.content.decode('utf-8'))
    if(len(trans_item_json) > 0):
        print("\n----------------------------------Transaction Detail----------------------------------\n")
        print("-------------------------------------------------------------------")
        print("|    Trans Id   |   Tip Value%   |    Discount    |  Total value  |")
        print("-------------------------------------------------------------------")
        for item in trans_item_json:
            print(
                f"|{item:^15}| {trans_item_json[item]['tip']:<15}| {trans_item_json[item]['discount']:<15}|{trans_item_json[item]['final_total']:<15}|")
        print("-------------------------------------------------------------------")
        while True:
            print("Please select following option:")
            print("1. Transaction detail\n2. Go to main menu")
            trans_choice = int(input())
            if trans_choice == 1:
                print("Enter Valid Transaction Id")
                trans_id = int(input())
                response = requests.post(
                    url + "get_trans_detail",
                    json={
                        'username': username,
                        'trans_id': trans_id})
                trans_detail_item_json = json.loads(
                    response.content.decode('utf-8'))
                if(len(trans_detail_item_json) > 0):
                    for item in trans_detail_item_json:
                        string = "Item " + str(trans_detail_item_json[item]['id']) + " [" + str(trans_detail_item_json[item]['plate']) + "] [" + str(
                            trans_detail_item_json[item]['quantity']) + "]: " + str(trans_detail_item_json[item]['item_value'])
                        print(string)
                    display_total_values(trans_item_json[str(trans_id)]['total'],
                                         trans_item_json[str(trans_id)]['tip'],
                                         trans_item_json[str(trans_id)]['discount'],
                                         trans_item_json[str(trans_id)]['each'],
                                         trans_item_json[str(trans_id)]['final_total'])
                else:
                    print("Wrong transaction Id Please try again")
            elif trans_choice == 2:
                break
            else:
                print("Wrong Choice Please try again")
    else:
        print("No old transaction detail")


if __name__ == "__main__":
    user_id = ""
    chef = 0
    while(1):
        while(user_id == ""):
            '''Asking participant to login or register'''
            print("Please choose following option")
            print("1. Login\n2. Register")
            login_choice = int(input())
            if login_choice == 1:
                user_id, chef = login()
            elif login_choice == 2:
                register()
            else:
                print("Wrong Choice Please try Again")
        '''After login we check it is regular customer or chef'''
        '''If it is chef it has one more function of adding data in menu table'''
        if(chef == 1):
            while(user_id != ""):
                print("Please choose following option")
                print("1. Order Food\n2. Change menu\n3. Old Transaction\n4. logout")
                chef_choice = int(input())
                if chef_choice == 1:
                    billmain()
                elif chef_choice == 2:
                    chef_menu_change()
                elif chef_choice == 3:
                    trans(user_id)
                elif chef_choice == 4:
                    user_id = ""
                    print("logout Successful")
                else:
                    print("Wrong Choice try again")
        else:
            while(user_id != ""):
                print("Please choose following option")
                print("1. Order Food\n2. old Transaction\n3. logout")
                user_choice = int(input())
                if user_choice == 1:
                    billmain()
                elif user_choice == 2:
                    trans(user_id)
                elif user_choice == 3:
                    user_id = ""
                    print("logout Successfull")
                else:
                    print("Wrong Choice please try again")
