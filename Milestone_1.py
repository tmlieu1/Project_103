"""
Milestone 1

This Milestone 1 of the CMPT 103 Programming project includes a variety of
functions that perform different tasks, but are all connected for the purpose
of displaying information about baby names in Alberta from 1980 - 2017.

load_file uses helper functions to process raw data from a file, creating
dictionaries of top ten lists and names per year.

data_splitter splits the data in the raw file into a more digestible format.

top_ten_dict creates a top ten dictionary consisting of top ten names for each
  corresponding year.

inner_top_ten_lists is a helper function for top_ten_dict which creates 
  separate inner dictionaries for boys and girls respectively.

names_dicts creates a dictionary of all names and the frequencies of each
  gender per year.

save_dicts saves the top ten dict and names dict into a pickled file.

load_pickle loads the top ten dict and names dict from a pickled file.

print_top_ten prints out the top ten dict based on user input in a digestible
  format.

name_search prints out the names dict based on user input in a digestible
  format.

main displays the menu, gets user choice, and executes it. main only quits if
  the user chooses to quit, otherwise, it waits for the user to select a valid
  option.

Author: Lou Lieu
"""
import pickle

def load_file(default):
    """
    Takes a default filename as a parameter. If the user does not input a
      filename, then the function opens the file with a default filename using
      a try/except. Once the file is opened, the file is split by lines and
      used to build two dictionaries dict_top_ten, and dict_name which are
      then returned.
    
    Parameter: 
    default: string
      A default filename string provided as the parameter.
    
    Return
    dict
      dict_top_ten - a dictionary of top ten names per year extracted from the 
        file. 
      dict_names - a dictionary of frequency of names per year extracted from
        the file.
    """
    
    dict_top_ten = {}
    dict_names = {}
    
    filename = input(f"Enter a file name [{default}]: ")
    
    '''
    If the filename provided is of NoneType or is an empty string, then
      the filename is set to the default parameter provided.
    '''
    if filename == None or filename == "":
        filename = default
    
    '''
    Try to open the file, if the file can't be opened, then return empty
      dictionaries.
    '''
    try:
        file = open(filename, 'r', encoding = 'utf-16')
        
    except:
        print("File does not exist")
        return dict_top_ten, dict_names
    
    #Splits the data into digestible format.
    data = file.readlines()
    data = data[5:]    
    split_data = data_splitter(data)
    
    #Builds top ten and names dictionaries.
    dict_top_ten = top_ten_dict(split_data)
    dict_names = names_dict(split_data)
    
    print("Data has been loaded and processed")
    return dict_top_ten, dict_names

def data_splitter(data):
    """
    Accepts a list 'data' as a parameter, splitting the strings in each line 
    into its own list with separated data. strip_data is then returned.
    
    Parameter: 
    data: list
      A list provided as the parameter.
    
    Return
    list
      strip - a formatted list consisting of baby data.
    """      
    strip_data = []
    
    '''
    For loop iterates through each item in data. The for loop then splits each
      item by '\t' and appends the item to strip_data list.
    '''
    for item in data:
        
        item = item[:-1].split('\t')
        item[0], item[2], item[4] = int(item[0]), int(item[2]), int(item[4])
        strip_data.append(item)

    return strip_data
    
def top_ten_dict(data):
    """
    Accepts a 'data' list as a parameter. The function makes use of a helper
      function to build a top ten dictionary per year by boy and girl keys.
      dict_top_ten is then returned.
    
    Parameter: 
    data : list
      A list provided as a parameter.
    
    Return
    dictionary
      dict_top_ten - A dictionary of format boy:[year:data], girl:[year:data].
    """
    dict_top_ten = {}
    dict_inner_boy = {}
    dict_inner_girl = {}
    
    #Helper function inner_top_ten_list used to generate boy and girl dicts.
    dict_inner = inner_top_ten_lists(data, "Boy", "Girl")

    '''
    For loop iterates through each item in data.
    
      if statements check to see if the index of value item[3] is "Boy" or 
      "Girl" before adding the item to the corresponding key.
    '''
    for item in data:
            
        if item[3] == 'Boy':
        
            dict_top_ten["boys"] = dict_inner[0]
            
        if item[3] == 'Girl':
                
            dict_top_ten["girls"] = dict_inner[1]
            
    return dict_top_ten

def inner_top_ten_lists(data, gender_boy, gender_girl):
    """
    Accepts a 'data' list, 'gender_boy' string, and a 'gender_girl' string as
      parameters. Corresponding boy and girl dictionaries are then built using
      the data provided. dict_inner_boy, and dict_inner_girl are then returned.
    
    Parameter: 
    data : list
      A list provided as a parameter.
    gender_boy : string
      A string provided as a parameter.
    gender_girl : string
      A string provided as a parameter.
    
    Return
    dictionary
      dict_inner_boy - A dictionary consisting of year key and 
        [rank, name, frequency] value.
      dict_inner_girl - A dictionary consisting of year key and 
        [rank, name, frequency] value.
    """    
    dict_inner_boy = {}
    dict_inner_girl = {}
    list_by_year_boy = []
    list_by_year_girl = []

    """
    For loop iterates through each item in data.
    
      Outer if checks to see whether the rank of the item is less than 10.
      
        First if checks to see if the gender in the item matches the gender
          supplied.
          
          Second if checks to see if the year is already a key in the dict.
            If it is, then the values up to item[:3] are appended to the value
            list.
          
          else statement occurs if the year is not already a key in the dict.
            It then adds the year as a key to the dict with list item[:3] 
            as the value.
            
        The second set of statements functions similarly to the first set.
    """
    for item in data:
        
        if item[0] < 11:
            
            if item[3] == gender_boy:
                
                if item[4] in dict_inner_boy:
                    
                    dict_inner_boy[item[4]].append(item[:3])
        
                else:
            
                    dict_inner_boy[item[4]] = [item[:3]]
            
            if item[3] == gender_girl:
                
                if item[4] in dict_inner_girl:
                    
                    dict_inner_girl[item[4]].append(item[:3])
                
                else:
                    
                    dict_inner_girl[item[4]] = [item[:3]]
        
    return dict_inner_boy, dict_inner_girl
    
def names_dict(data):
    """
    Accepts a 'data' list, as a parameter. A dictionary consisting of keys of
       names with [frequency, gender, year] values is then built and returned.
    
    Parameter: 
    data: list
      a list provided as a parameter.
    
    Return
    dictionary
      dict_name - A dictionary with key names with [frequency, gender, year]
        values.
    """

    dict_name = {}
    
    '''
    for loop iterates through the data.
      
      if statement checks to see if the name is a dict_name dictionary key.
        If it is, then the [frequency, gender, year] of the current item
        iteration is appended to the value list.
    
      else statement occurs if the name isn't a dict_name dictionary key.
        It then adds the key to the list with the current item's 
        [frequency, gender, year] as the value.
    '''
    for item in data:

        if item[1] in dict_name:
            dict_name[item[1]].append(item[2:])
            
        else:
            dict_name[item[1]] = [item[2:]]
    
    return dict_name
    
def save_dicts(default, top_ten, names):
    """
    Accepts 'default' string, 'top_ten' dict, and 'names' dict as parameters.
      If the user doesn't input a filename, then the default filename is used.
      The function then writes the two dictionaries into a pickled file.
    
    Parameter: 
    default: string
      A string provided as a parameter.
    top_ten: dictionary
      A dictionary provided as a parameter.
    names: dictionary
      A dictionary provided as a parameter.
    
    Return
    None
    """
    
    dicts = [top_ten, names]
    filename = input(f"Enter a file name [{default}]: ")
    
    '''
    If the filename provided is of NoneType or is an empty string, then
      the filename is set to the default parameter provided.
    '''
    if filename == None or filename == "":
        filename = default
    
    pickle.dump(dicts, open(filename, "wb"))
    print(f"Saved pickled data in {filename}.")

def load_pickle(default):
    """
    Takes a default filename as a parameter. If the user does not input a
      filename, then the function opens the pickled file with a default filename 
      using a try/except. dict_top_ten, and dict_name which are then returned.
    
    Parameter: 
    default: string
      A default filename string provided as the parameter.
    
    Return
    dict
      dict_top_ten - a dictionary of top ten names per year extracted from the 
        file. 
      dict_names - a dictionary of frequency of names per year extracted from
        the file.
    """
    dicts = {}
    dict_top_ten = {}
    dict_names = {}
    
    filename = input(f"Enter a file name [{default}]: ")
    
    '''
    If the filename provided is of NoneType or is an empty string, then
      the filename is set to the default parameter provided.
    '''
    if filename == None or filename == "":
        filename = default    
    
    '''
    try to open the pickled file, and assign it to dicts. If there is an error,
      instead return None.
    '''
    try:
        dicts = pickle.load(open(filename, "rb"))
        
    except:
        print("File does not exist")
        return
    
    print(f"Loaded pickled data from {filename}.")
    dict_top_ten, dict_name = dicts
    
    return dict_top_ten, dict_name

def print_top_ten(dict_top_ten):
    """
    Accepts a dictionary dict_top_ten as a parameter. The function then accepts
      b or g input from the user, and year input from the user. The input
      variables are then used to print out the top 10 names for the gender
      in alberta for the given year.
    
    Parameter: 
    dict_top_ten: dictionary
      A dictionary provided as a parameter.
    
    Return
    None
    """
    print_top_ten = {}
    gender = ""
    print_out = ""

    b_or_g = input("Enter B for boy's names or G for girl's names: ").lower()
    
    '''
    While the user choice for gender isn't b or g, then the user is prompted
      again.
    '''
    while b_or_g != 'b' and b_or_g != 'g':
        
        b_or_g = input("Enter B for boy's names or G for girl's names: ").lower()
        
    user_year = input("Enter year (1980 to 2017): ")
    
    '''
    While the user choice is not a digit or it's a digit greater than 2017 or
      less than 1980, the user is prompted again.
    '''
    while user_year.isdigit() == False or int(user_year) > 2017 or int(user_year) < 1980:
        
        user_year = input("Enter year (1980 to 2017): ")
    
    user_year = int(user_year)
    
    '''
    If statements perform similarly. If the user input is 'g', then the
    gender is set to 'girls'. If the user input is 'b', then the gender is set
    to 'boys'.
    '''
    if b_or_g == 'g':
        
        gender = "girls"
        
    if b_or_g == 'b':
        
        gender = "boys"
        
    print(f"\nTop 10 names for baby {gender} born in Alberta in {user_year}:")    
    
    '''
    Outer for loop iterates through the keys and values in dictionary
    dict_top_ten.
      
      Inner for loop iterates through numbers 0-10 (not including).
        
        If statement checks to see if the key is equal to the gender provided
          by the user. If it is, then it prints out the top ten list of the
          gender for the provided year.
    '''
    for key, value in dict_top_ten.items():
        for num in range(len(dict_top_ten.get(gender).get(user_year))):
            
            if key == gender:
                print(f"\t{dict_top_ten.get(gender).get(user_year)[num][0]}", 
                      dict_top_ten.get(gender).get(user_year)[num][1], 
                      dict_top_ten.get(gender).get(user_year)[num][2])

def name_search(dict_names):
    """
    Accepts a dictionary dict_names as a parameter. The function then accepts
      a baby name from the user. The function then prints out the frequency
      of that name for boys and girls per year.
    
    Parameter: 
    dict_names: dictionary
      A dictionary provided as a parameter.
    
    Return
    None
    """
    freq_b = 0
    freq_g = 0
    
    user_name = input("Enter a name: ").title()
    
    '''
    If the value of the key of dict_names is empty, then the user is informed
      and the function returns None.
    '''
    if dict_names.get(user_name) == None:
        
        print(f"There were no babies named {user_name} born in Alberta\
 between 1980 and 2017")
        return    
    
    print(f"\n{user_name}:\n\tBoys\tGirls")
    
    '''
    For loop iterates through the years 1980 - 2018.
      
      Outer if continues if the value of the key at user_name isn't None.
      
        Inner for loop iterates through the range of the length of the
          dict_names.
          
          Inner if statement checks to see if the year in dict_names is equal
            to the year of the outer for loop.
            
            First inner if statement checks to see if the gender in dict_names
              is boy.
            
            Second inner if statement checks to see if the gender in dict_names
              is girl.
        
        Second if statement prints as long as the frequency of boy and girl
          is not 0.
    '''
    for year in range (1980, 2018):
        
        freq_b = 0
        freq_g = 0        
        
        if dict_names.get(user_name) != None:
                
            for num in range(len(dict_names.get(user_name))):
            
                if int(dict_names.get(user_name)[num][2]) == year:
                
                    if dict_names.get(user_name)[num][1] == "Boy":
                        freq_b = dict_names.get(user_name)[num][0] 
                
                    if dict_names.get(user_name)[num][1] == "Girl":
                        freq_g = dict_names.get(user_name)[num][0]
                        
        if (freq_b != 0 or freq_g != 0):    
            print(f"{year}\t{freq_b}\t{freq_g}")

def display_text():
    """
    Displays the menu so it doesn't take up a lot of room when written.
    
    Parameter:
    None
    
    Return
    None
    """
    
    print(f"\nAlberta Baby names 1980 to 2017\
\n-------------------------------\
\n(0) Quit\
\n(1) Load and process text file\
\n(2) Save processed data\
\n(3) Open processed data\
\n(4) Print top ten lists\
\n(5) Search for a name\
\n(6) Names that appear only once in a year\
\n(7) Longest name\
\n(8) Search for names with specific letters\
")            
    
def get_unique_names(names_dict):
    """
    Definition
    
    Parameter: 
    None
    
    Return
    None
    """    
    user_year = input("Enter a year (1980 - 2017): ")
    boy_list = []
    girl_list = []
    count = 0
    max_boy = 0
    max_girl = 0
    
    while user_year.isdigit() == False or int(user_year) > 2017 or int(user_year) < 1980:
        
        user_year = input("Enter a year (1980 - 2017): ")
    
    user_year = int(user_year)
    
    for key, value in names_dict.items():
        
        for item in value:
            
            if item[2] == user_year and item[0] == 1:
                
                if item[1] == 'Boy':
                    
                    boy_list.append(key)
                    if len(key) > max_boy:
                        max_boy = len(key)
                        
                if item[1] == 'Girl':
                    
                    girl_list.append(key)
                    if len(key) > max_girl:
                        max_girl = len(key)
    
    max_boy = max_boy - max_boy % 8
    max_girl = max_girl - max_girl % 8
    
    for boy in boy_list:
        count += 1
        
        
    
    '''
    for boy in boy_list:
        count += 1
        
        if len(boy) >= 24:
            print(boy, end = "\t")
        
        if len(boy) >= 16 and len(boy) < 24:
            print(boy, end = "\t\t")
            
        if len(boy) >= 8 and len(boy) < 16:
            print(boy, end = "\t\t\t")
                
        if len(boy) < 8:
            print(boy, end = "\t\t\t\t")
            
        if count % 4 == 0:
            print()
    '''
    
def longest_names(names_dict):
    return

def wildcard_search(names_dict):
    return

def main():
    """
    The function displays the menu, gets the menu choice from the user, and
      executes the user's choice. If the user chooses 0, then the user quits.
    
    Parameter: 
    None
    
    Return
    None
    """
    dict_top_ten = {}
    dict_names = {}
    display_text()
    user_choice = input("\nEnter command: ")
    
    '''
    While loop runs as long as the user doesn't choose 0, choose "", or the
      choice is of NoneType.
      
      if loop 1 runs the load_file function with default parameter.
      
      if loop 2 runs the save_dicts function with default parameter.
      
      if loop 3 runs the load_pickle function with default parameter.
      
      if loop 4 runs the print_top_ten function.
      
      if loop 5 runs the name_search function.
    '''
    while user_choice != "0" or user_choice == "" or user_choice == None:

        if user_choice == "1":
            dict_top_ten, dict_names = load_file("baby-names-frequency-2017.txt")
            #dict_top_ten, dict_names = load_file("test_data.txt")
            
        if user_choice == "2":
            save_dicts("baby_names.p", dict_top_ten, dict_names)
        
        if user_choice == "3":
            dict_top_ten, dict_names = load_pickle("baby_names.p")
            
        if user_choice == "4":
            print_top_ten(dict_top_ten)
            
        if user_choice == "5":
            name_search(dict_names)
            
        if user_choice == "6":
            get_unique_names(dict_names)
        
        if user_choice == "7":
            longest_names(names_dict)
        
        if user_choice == "8":
            wildcard_search(names_dict)
        
        display_text()
        user_choice = input("\nEnter command: ")
    
    '''
    If the user choice is 0, the function returns none (exits) and prints
      Goodbye.
    '''
    if user_choice == "0":
        print("Goodbye")
        
    return

main()