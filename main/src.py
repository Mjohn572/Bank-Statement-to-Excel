import re

"""
TO USE, CREATE NEW TEXT FILE, DO CTRL+SHIFT+P AND TYPE IN 'EXTRACT TEXT FROM PDF', THEN SELECT BANK STATEMENT PDF FILE
"""

def write_to_categories_txt(categories_to_add: list) -> None:
    """
    This Function has 4 Stages:
    1. Grabbing category list used in previous function & instantiating the a just category list
    2. Retreiving each category from the full list into its own list
    3. Retreiving each transaction place to add and the corresponding category and matching it to see if it is present. 
    Either way it is added into the list either into the first slot of the matching category, or into its own new category.
    4. Writing the list over top of the categories.txt file
    """

    # Retrieve file used to get categories before
    categories_txt_list = read_file('main/categories.txt')

    # Inst all categories into a list, to ensure checking is smooth
    just_categories = []
    
    # Retrieving each line in the list
    for indx, line in enumerate(categories_txt_list):

        # Capturing all categories and putting them into one list
        just_categories.append(categories_txt_list[indx][len(line)-1])


    # Retrieving each line in list of cats to add
    for line_to_add in categories_to_add:

        # Retrieving each item in list of cats to add
        #for item_to_add in line_to_add:
            
        # Checking if the category retreived matches any category in the cat list
        if line_to_add[1] in just_categories:

            # Retreiving the index where they match
            indx_of_category = just_categories.index(line_to_add[1])

            # Inserting transaction place into the first column of the matching category
            categories_txt_list[indx_of_category].insert(0, line_to_add[0])

        # If there is no category matching 
        else: 
            # Adds new category to ongoing category list
            just_categories.append(line_to_add[1])

            # Adds new items to ongoing transaction place and category list
            categories_txt_list.append([line_to_add[0], line_to_add[1]])

    #Opening file to write over
    file_status = open('main/categories test.txt', "w")

    # Writing out full new category database
    for indx, line in enumerate(categories_txt_list):
        for item in line:
            file_status.write(item)
            file_status.write(',')
        if indx != len(categories_txt_list) - 1:
            file_status.write('\n')



def category_list(cleaned_list: list) -> list:
    """
    
    """
    # Inst final list
    list_w_cats = []

    # Inst list of categories and places to add into txt file
    categories_to_write = []

    # Retrieve category database file
    categories_txt_list = read_file('main/categories.txt')

    #TEST
    print(categories_txt_list)

    # Retreieve the index of the cleaned_list
    for i in range(len(cleaned_list)):

        # Retreive the transaction place from the current line
        transaction_place = cleaned_list[i][1]

        # Inst/reset checker for which category the trans place belongs to
        category_to_append = ""

        # Retreive line from txt file
        for line in categories_txt_list:
            
            # Retreive item from txt file
            for item in line:
                
                # If the transaction place is present in the line
                if item in transaction_place:

                    # Makes category_to_append to the last item in the list, which is the category
                    category_to_append = line[len(line) - 1]

        # If category_to_append has something in it, it runs
        if category_to_append:
            
            # Adds all of the items from the cleaned_list to the new list, with the category at the end
            list_w_cats.append([cleaned_list[i][0], cleaned_list[i][1], cleaned_list[i][2], category_to_append])

        else:
            # Printing for user
            print("-----------------------------------------------------------------------------------")
            print("Categories: ")

            # Retreiving all the indicies of the Category Text List
            for line in range(len(categories_txt_list)):

                # Printing all of the last index of in each line, which is each category
                print(categories_txt_list[line][len(categories_txt_list[line])-1])
                
            # Printing for user
            print("-----------------------------------------------------------------------------------")

            # Printing the transaction place 
            print("Transaction Place: " + cleaned_list[i][1])

            # Asking the user which category it belongs to, and making it uppercase
            user_input_category = input("What category does this transaction belong to? ")
            user_input_category = user_input_category.upper()
            print(user_input_category)

            # Adds the transaction place and new category from user into a list to later be given to the writing function
            categories_to_write.append([cleaned_list[i][1], user_input_category])
                
            # Adds all of the items from the cleaned_list to the new list, with the category at the end
            list_w_cats.append([cleaned_list[i][0], cleaned_list[i][1], cleaned_list[i][2], user_input_category])
            
    # Calls writing function and gives a list that contains every transaction place and category to be put into database
    write_to_categories_txt(categories_to_write)

    return list_w_cats

def clean_list(file_contents: list) -> list:

    
    cleaned_list = [] # Instantiating the final list

    for i in range(len(file_contents)): # Check through each index one by one

        if "RETAIL PURCHASE" in file_contents[i] or "E-transfer" in file_contents[i] or "PREAUTHORIZED DEBIT" in file_contents[i]:
        
            # Regex to match a date at the beginning of the string (e.g., 'Nov 1', 'Dec 25', etc.)
            # and remove everything after it
            result = re.search(r'^[A-Za-z]{3} \d{1,2}', file_contents[i])

            # Extract the date part and store it
            if result: # The First one should always return with a date
                date = result.group()

            else:
                date = cleaned_list[-1][0] if cleaned_list else "Unknown" # If no match, take date from previous append, if no previous date make Unknown
            

            transaction_place = file_contents[i+1] # Add the next line, which is the retail place


            if "CAD" in file_contents[i+2] or "USD" in file_contents[i+2] or "CAPPED MONTHLY FEE$16.95" in file_contents[i+2] or "eBay Commerce Ca" in file_contents[i+2]: # Checking if this line is a throwaway
                # If line was throwaway get next line
                purchase_amount = file_contents[i+3]
            else:  
                # If no throwaway line get index 2
                purchase_amount = file_contents[i+2]
            
            # Truncate the purchased amount to only get the first number without rounding
            purchase_amount_truncated = str(int(float(purchase_amount.split(',')[0]) * 100) / 100)

            cleaned_list.append([date, transaction_place, purchase_amount_truncated])

    return cleaned_list

def read_file(file_name: str) -> list:
    """
    To read the file and return its contents
    """
    file_open = open(file_name, "r")
    input_file = file_open.readlines()
    file_list = []
    if "StatementText.txt" in file_name:
        for line in input_file:
            file_list.append(line.strip())
    else:
        for line in input_file:
            file_list.append(line.strip().split(','))
    
    file_open.close()

    return file_list

def main() -> None:
    """
    Here is where everything starts and ends. 
    All functions will be called in this function
    """
    
    file_name = "main/StatementText.txt"

    #Takes the contents of the file and adds it to a list where every index is a line
    file_contents = read_file(file_name)

    #print(file_contents) # To TEST
    cleaned_list = (clean_list(file_contents))
    print(cleaned_list)
    print(category_list(cleaned_list))

main()