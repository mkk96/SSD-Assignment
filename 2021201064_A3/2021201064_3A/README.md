File Name: bill.py
To Run file: python bill.py

Prerequisite: 
	Python should be install in system
	
Assumption:
	Python program can be run using "python" command
	bill.py and menu.csv file is in same folder
	
This program is interactive program which take input from user to get end result.

After running the program user will get menu in item id half plate full plate price and entry
seperated by tab.
User need to enter the order in item id plate type quantity format. User can enter any number of
entries it can be exit by pressing enter two times.
After enter menu program will ask user to select tip percentage. User will given 3 option 0% 10% 20%
user need to select one of these by selecting 1,2 or 3.

Now program will display total price of item including tip value.
Now, program will ask user to enter number of people to share this bill. After user will some valid number
it will display total share of each person.

User will asked whether they want to participate test your luck skill. Based on user input 
program will foloow two path either display final values if enter no or enter contest if enter yes

if select yes one program will genrate random number if number if fall between
1 to 5 user will get 50% discount
6 to 15 user will get 25% discount
16 to 30 user will get 10% discount
31 to 50 user will get 0% discount
51 to 100 price will increase by 20%

after calculating discount or increase program will display increase or discount value.

After that or if user type "No" below are item it will display
Total price of each item with item id [plate type] [quantity]: total price format
Total price exculding tip value.
Tip percentage which user selected
Discount or increase value from contest if took part if user didn't took part then 0 will print
Final price including item price+tip valu + discount/increase value
and finally updated share of each person