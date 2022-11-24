import helper_functions 

if __name__ == "__main__":
    data = helper_functions.read_JSON_file() # read file 

    date = data[len(data)-1]["date"] if data != [] else "27 Jan 2006" # fetch latest or default date
    cabinent_statements = helper_functions.get_cabinent_statements_urls(date) #read cabinet statements until

    for statement in reversed(cabinent_statements): #reverse the order to store in descending order
        extracted = helper_functions.extract_translations(statement['url']) #try extract for each url
        if extracted: data.append(extracted) #if successful append to current data

    helper_functions.write_JSON_file(data) # write file
