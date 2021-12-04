import csv
import random


def get_data_from_csv_file():
    '''Reading Menu csv file and genrating 2d list which containg menu from csv and
returning the csv'''
    menu_file = open("menu.csv")
    menu_item_from_csv_file = csv.reader(menu_file)
    menu_header = next(menu_item_from_csv_file)
    item_list = []
    for row_item in menu_item_from_csv_file:
        item_list.append(row_item)
    menu_file.close()
    return item_list, menu_header


def display_menu(item_list, menu_header):
    '''Display the menu which we got after reading the csv file'''
    print("\n----------------------------------Menu----------------------------------\n")
    print("---------------------------------------------------")
    print(
        f"|{menu_header[0]:^15}| {menu_header[1]:<15}| {menu_header[2]:<15}|")
    print("---------------------------------------------------")
    for item in item_list:
        print(f"|{item[0]:^15}| {item[1]:<15}| {item[2]:<15}|")
    print("---------------------------------------------------")


def input_from_user():
    '''Taking menu input from user in Item no   Plate type  Quantity formate
    user can enter any number of order and to exit they need to enter two times'''
    print("Please Enter your order info( Item no   Plate type  Quantity):\n")
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
    for menu_result_list_row in menu_result_list:
        string = "Item " + str(menu_result_list_row[0]) + " [" + str(menu_result_list_row[1]) + "] [" + str(
            menu_result_list_row[2]) + "]: " + str(menu_result_list_row[3])
        print(string)


if __name__ == "__main__":
    '''this function is used to read data from CSV and store header in header list and menu
        in item list variable'''
    item_list, menu_header = get_data_from_csv_file()

    '''After getting header and value from above function below function is used to
        display in tab sepearted format'''
    display_menu(item_list, menu_header)

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

    '''Displaying total price excluding tip, tip percentage, discount/increase amount
        if they participated in scheme, final total price and updated share of each person'''
    print("Total:", "{:.2f}".format(total_price))
    print("Tip Percentage:" + str("{:.2f}".format(tip_percentage) + "%"))
    print(
        "Discount/Increase:",
        "{:.2f}".format(
            discount_from_scheme *
            total_price_with_tip /
            100))
    print(
        "Final Total:",
        "{:.2f}".format(
            total_price_with_tip +
            discount_from_scheme *
            total_price_with_tip /
            100))
    each_person_share = (total_price_with_tip + discount_from_scheme *
                         total_price_with_tip / 100) / people_to_split_bill
    print("\n----------------------------------------")
    print("Share for each person is", "{:.2f}".format(each_person_share))
    print("----------------------------------------\n\n")
