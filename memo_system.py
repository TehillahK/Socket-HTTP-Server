#   memo_system.py
#   Tehillah Kangamba 7859367   
#   Comp3010
#   Assignment 2
#   This class is the memo system ,it creates and deletes memos
import uuid

class Memo:
    def __init__(self) :
        self.database = {}

    #   get_all
    #   gets all memos from the database
    def get_all(self):
        return self.database

    #   create_memo
    #   adds and updates memo into the database
    #   accepts a string memo as a paramater
    def create_memo(self ,memo):
        result = False
        memo_id = uuid.uuid4
        self.database[memo_id] = memo
        if memo_id in self.database:
            result = True
        return result
    
    #   delete_memo
    #   checks if memo is in database and if so deletes
    #   accepts one param id which is a string 
    #   returns true if its successsful and False otherwise
    def delete_memo(self,id):
        result = False
        if id in self.database:
            self.database.pop(id)
            result = True
        return result

