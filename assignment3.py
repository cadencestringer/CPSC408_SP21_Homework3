import sqlite3
import pandas as pd
from pandas import DataFrame

# https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
# https://www.programiz.com/python-programming/methods/string/isspace

conn = sqlite3.connect('./assignment3.sqlite')
myCursor = conn.cursor()
colNames = ['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State',
            'ZipCode', 'MobilePhoneNumber', 'isDeleted']


# Checks if a letter exists in the string, to check if phone numbers are all numeric/special chars
def valid_input(val):
    return val == "1" or val == "2" or val == "3" or val == "4" or val == "5"


# Checks if a string has digits, to check if names/city/state etc. are entered correctly
def has_digit(input_string):
    return any(char.isdigit() for char in input_string)


# Checks if a letter exists in the string, to check if phone numbers are all numeric/special chars
def has_letter(input_string):
    return any(char.isalpha() for char in input_string)


# For GPA inputs, checks if each char in the string is numeric or a decimal point
def is_decimal(input_string):
    return any(char.isdigit() or char == '.' for char in input_string)


# Function to print the initial menu and return what the user selects
def print_menu():
    selected = input("What option would you like to execute? Enter 1, 2, 3, 4, or 5:"
                     "\n\t1. Display all students/attributes"
                     "\n\t2. Add new students"
                     "\n\t3. Update students"
                     "\n\t4. Delete students by ID"
                     "\n\t5. Search for a student by Major, GPA, City, State and Advisor"
                     "\nOR press any other key to exit. \n")
    return selected


# Functions to get input from the user, including error checking (while loops to ensure
# the appropriate input is entered)

def get_ID_input():
    student_id_input = input("Enter student ID: \n")
    while not student_id_input.isdigit():
        student_id_input = input("Please enter a NUMERIC Student ID: \n")
    return student_id_input


def get_firstname_input():
    first_name_input = input("Enter first name: \n")
    while not first_name_input.isalpha():
        first_name_input = input("Please enter TEXT (non-numeric/no special chars) for first name: \n")
    return first_name_input


def get_lastname_input():
    last_name_input = input("Enter last name: \n")
    while not last_name_input.isalpha():
        last_name_input = input("Please enter TEXT (non-numeric/no special chars) for last name: \n")
    return last_name_input


def get_gpa_input():
    GPA_input = input("Enter GPA: \n")
    while not is_decimal(GPA_input):
        GPA_input = input("Please enter a NUMERIC GPA with a decimal point: \n")
    return GPA_input


def get_major_input():
    major_input = input("Enter major: \n")
    while has_digit(major_input):
        major_input = input("Please enter TEXT (non-numeric) for major: \n")
    return major_input


def get_advisor_input():
    advisor_input = input("Enter faculty advisor: \n")
    while has_digit(advisor_input):
        advisor_input = input("Please enter TEXT (non-numeric) for faculty advisor: \n")
    return advisor_input


def get_city_input():
    city_input = input("Enter city: \n")
    while has_digit(city_input):
        city_input = input("Please enter TEXT (non-numeric) for city: \n")
    return city_input


def get_state_input():
    state_input = input("Enter state: \n")
    while not state_input.isalpha():
        state_input = input("Please enter TEXT (non-numeric/no special chars) for state: \n")
    return state_input


def get_zipcode_input():
    zipcode_input = input("Enter zipcode: \n")
    while not zipcode_input.isdigit():
        zipcode_input = input("Please enter numbers for zipcode: \n")
    return zipcode_input

# Read in the data from students.csv
def read_csv(fileName):
    path = "./"
    filePath = path + fileName
    with open(filePath) as inputFile:
        columns = inputFile.readline()  # get column names
        data = inputFile.readlines()  # get the rest of the data

    for i in range(len(data)):
        data[i] = data[i].strip().split(',')
        myCursor.execute("INSERT INTO Student ('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State',"
                         "'ZipCode', 'MobilePhoneNumber', 'isDeleted') VALUES(?,?,?,?,?,?,?,?,?,?,?);",
                         (data[i][0], data[i][1], data[i][8], data[i][7], "NULL", data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], 0))
        conn.commit()

read_csv("students.csv")


# Application options:

def option1():
    myCursor.execute('SELECT * FROM Student;')
    myRecords = myCursor.fetchall()
    df = DataFrame(myRecords, columns=[colNames])
    print(df)


def option2():
    # Gets all input
    studentIDInput = get_ID_input()
    firstNameInput = get_firstname_input()
    lastNameInput = get_lastname_input()
    GPAInput = get_gpa_input()
    majorInput = get_major_input()
    facultyAdvisorInput = get_advisor_input
    addressInput = input("What is the student's address? \n")
    cityInput = get_city_input()
    stateInput = get_state_input()
    zipcodeInput = get_zipcode_input()
    mobilePhoneNumberInput = input("Enter mobile phone number: \n")

    # Inserts row into Student table
    myCursor.execute('INSERT INTO Student VALUES (?,?,?,?,?,?,?,?,?,?,?,?);',
                     (studentIDInput, firstNameInput, lastNameInput, GPAInput, majorInput, facultyAdvisorInput,
                      addressInput, cityInput, stateInput, zipcodeInput, mobilePhoneNumberInput, 0,))
    conn.commit()


def option3():
    studentIDInput = get_ID_input()
    selection = input("Would you like to update major, advisor, or mobile phone number? (1 ,2, or 3) \n")
    while not (selection == "1" or selection == "2" or selection == "3"):
        selection = input("Please enter 1, 2, or 3: \n")

    # Depending on what the user selects, prompts for additional info and updates that row
    # using student ID
    if selection == "1":
        majorInput = get_major_input()
        myCursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?;",
                         (majorInput, studentIDInput,))
        conn.commit()

    elif selection == "2":
        facultyAdvisorInput = get_advisor_input()
        myCursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?;",
                         (facultyAdvisorInput, int(studentIDInput),))
        conn.commit()

    elif selection == "3":
        mobilePhoneNumberInput = input("Enter mobile phone number: \n")
        myCursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?;",
                         (mobilePhoneNumberInput, int(studentIDInput),))
        conn.commit()


def option4():
    studentIDInput = get_ID_input()
    # Completes soft delete using isDeleted column and student ID
    myCursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?;",
                     (studentIDInput,))
    conn.commit()


def option5():
    selection = input("Would you like to display by major, GPA, city, state, or advisory? (1 ,2, 3, 4, or 5) \n")
    while not valid_input(selection):
        selection = input("Please enter 1, 2, 3, 4, or 5: \n")

    if selection == "1":
        majorInput = get_major_input()
        myCursor.execute("SELECT * FROM Student WHERE Major = ?;",
                         (majorInput,))
    elif selection == "2":
        GPAInput = get_gpa_input()
        myCursor.execute("SELECT * FROM Student WHERE GPA = ?;",
                         (GPAInput,))
    elif selection == "3":
        cityInput = get_city_input()
        myCursor.execute("SELECT * FROM Student WHERE City = ?;",
                         (cityInput,))
    elif selection == "4":
        stateInput = get_state_input()
        myCursor.execute("SELECT * FROM Student WHERE State = ?;",
                         (stateInput,))
    elif selection == "5":
        advisorInput = get_advisor_input()
        myCursor.execute("SELECT * FROM Student WHERE Advisor = ?;",
                         (advisorInput,))

    myRecords = myCursor.fetchall()
    df = DataFrame(myRecords, columns=[colNames])
    if df.empty():
        print("No students match your inputs.")
    else:
        print(df)

# Run application:
menuSelection = print_menu()
while valid_input(menuSelection):
    pd.set_option('display.max_columns', None)
    if menuSelection == "1":
        option1()
    elif menuSelection == "2":
        option2()
    elif menuSelection == "3":
        option3()
    elif menuSelection == "4":
        option4()
    elif menuSelection == "5":
        option5()
    menuSelection = print_menu()

print("Quitting Student Database. Thanks for visiting!")
conn.close()