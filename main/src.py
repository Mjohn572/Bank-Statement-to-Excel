import re

def clean_list(file_contents: list) -> list:

    cleaned_list = []
    for i in file_contents:
        if "RETAIL PURCHASE" or "E-transfer" not in file_contents[i]:
            file_contents.remove(i)
        else:
            # Regex to match a date at the beginning of the string (e.g., 'Nov 1', 'Dec 25', etc.)
            # and remove everything after it
            result = re.search(r'^[A-Za-z]{3} \d{1,2}', file_contents[i])

            # Extract the date part and store it
            if result:
                cleaned_list.append(result.group())

            else:
                cleaned_list.append(cleaned_list[i-2]) # If no match, take date from previous append

            
            cleaned_list.append(file_contents[i+1]) # Add the Reail Place
            
            cleaned_list.append(file_contents[i+2]) # Add the Amount

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
    file_name = "main/test.txt"
    file_contents = read_file(file_name)
    print(file_contents)


    #Create List
    # if line has Retail Purchase OR E-Trasnfer
    #Create list of list and append into inital list
    # NextLine(IF line has CAD or USD)
    #
    #NextLine(Take the number with only 2 decimals, no rounding)
    # if line has Deposit OR Pay
main()