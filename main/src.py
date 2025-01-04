import re
"""
TO USE, CREATE NEW TEXT FILE, DO CTRL+SHIFT+P AND TYPE IN 'EXTRACT TEXT FROM PDF', THEN SELECT BANK STATEMENT PDF FILE
"""
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
    for line in input_file:
        file_list.append(line.strip())
    
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

    print(clean_list(file_contents))

main()