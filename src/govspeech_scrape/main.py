import helper_functions

if __name__ == "__main__":
    data = helper_functions.read_JSON_file() # read file 
    date = data[len(data)-1]["date"] if data != [] else "14 Mar 2013" # fetch latest or default date
    cabinent_statements = helper_functions.get_cabinent_statements_urls(date) #read cabinet statements until date

    new_data = []
    for statement in reversed(cabinent_statements): #reverse the order to store in descending order
        print('----------------------------')
        extracted = helper_functions.extract_translations(statement['url']) #try extract for each url
        if extracted: new_data.append(extracted) #if successful append to current data

    helper_functions.update_all_csv(new_data)
    helper_functions.write_JSON_file(data+new_data) # write file (data+new_data will concat the lists)
