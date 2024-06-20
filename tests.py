import requests


BASE = "http://127.0.0.1:5000/"
s = input("ADD: a , UPDATE : b , DELETE : c , PRINT : d , PRINT ALL : e, EXIT : x ")

while s!='x':

    
    
    #adding a new book to the database
    if s=='a':
        title = input("Input title : ")
        author = input("Input author : ")
        publishing_date = input("Published Date : ")
        new_book = {
            "title": title,
            "author": author,
            "published_date": publishing_date 
        
        }
        try:
            response = requests.post(BASE + "api/book", json=new_book, headers={'Content-Type': 'application/json'})
        except requests.exceptions.RequestException as e:
            print(f"An error occured : {e}")
        print(response.text)

    #updating an existing database
    elif s=='b':
        title = input("Input title : ")
        author = input("Input author : ")
        publishing_date = input("Published Date : ")
        new_book = {
            "title": title,
            "author": author,
            "published_date": publishing_date 

        }
        x = input("Book id you want to update : ")
        
        try:
            response = requests.put(BASE + "api/book/"+ x, json=new_book, headers={'Content-Type': 'application/json'})
        except requests.exceptions.RequestException as e:
            print(f"An error occured : {e}")
        print(response.text)


    #deleting an existing record of the database
    elif s=='c':
        y = input("Book id you want to update : ")
        
        try:
            response = requests.delete(BASE + "api/book/"+ y)
        except requests.exceptions.RequestException as e:
            print(f"An error occured : {e}")
        print(response.text)
        

    #for printing specific book
    elif s=='d':
        z = input("Book ID you want to print : ")
        
        try:
            response = requests.get(BASE + "api/book/"+ z)
        except requests.exceptions.RequestException as e:
            print(f"An error occured : {e}")
        print(response.text)

    #print all the books
    elif s=='e':
        
        try:
            response = requests.get(BASE + "api/books")
        except requests.exceptions.RequestException as e:
            print(f"An error occured : {e}")
        print(response.text)

    elif s==0:
        break

    else:
        print("Enter Valid Input!")

    s = input("ADD: a , UPDATE : b , DELETE : c , PRINT : d , PRINT ALL : e, EXIT : x ")






