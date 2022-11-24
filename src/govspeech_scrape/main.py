import helper_functions 

if __name__ == "__main__":
    data = helper_functions.read_JSON_file()

    date = data[len(data)-1]["date"] if data != [] else "19 Aug 2021" 
    cabinent_statements = helper_functions.get_cabinent_statements_urls(date)

    for statement in reversed(cabinent_statements):
        extracted = helper_functions.extract_translations(statement['url'])
        if extracted: data.append(extracted)  

    helper_functions.write_JSON_file(data)
