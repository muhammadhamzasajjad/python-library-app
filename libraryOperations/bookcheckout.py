#Author: Muhammad Hamza Sajjad
#Date:20/11/2019
#last update:09/12/2019

"""
    this module contains function to checkout
    a book by a given member id. In real world when a librarian does a checkout
    he does not have to provide the checkout date and that is exactly what I
    will do. i.e. the system will automatically put today's date as checkout
    date
"""


from sys import path
from os.path import abspath,dirname,join
thisDir = dirname(abspath(__file__))

path.append(join(thisDir,"data"))
import database
from datetime import datetime


def checkMemId(memId):
    '''return true only if memberId is a 4 digit number otherwise returns false
    :param memId is and integer representing the memberId
    '''
    
    return  isinstance(memId,int) and memId>=1000 and memId<=9999


def performCheckout(bookId, memId):
    """The function takes a bookId, a memberId if the parameter values are
    correct it performs the checkout and saves it in the file. Raises exception
    if parameter values are not correct
    :param bookId: is the id of the book to be checkedout
    :param memId: is the id of the member who wants checkout the book
    """

    BooksDic=database.getBooks()
    checkoutLogs=database.getLogData()
    rtnmsg=""
    
    if not checkMemId(memId):
        raise Exception("Member Id not valid")
    
    elif bookId not in BooksDic:
        raise Exception("book Id "+str(bookId)+" does not exist")
    
    elif BooksDic[bookId][3]!=0:
        raise Exception("book with id "+str(bookId)+" is already borrowed "\
                        "by someone")
    
    else:
        BooksDic[bookId][3]=memId
        
        #when the librarian checksout a book the system will put
        #automatically today's date.
        todayDateStr=datetime.now().strftime("%d/%m/%Y")
        row=database.listToString([bookId,todayDateStr,"--"])
        database.appendline("logfile.txt",row)
        
        checkoutLogs.append([bookId,todayDateStr,"--"])
        
        database.writeFile("database.txt",
                           database.toTableStrWithoutHeading(BooksDic))
    return BooksDic

def test():
    """tests all of the functions of this module
    and gives their result on command line
    """
    
    booksDic1=database.getBooks()
    logs1=database.getLogData()
    bookId=list(booksDic1.keys())[0]
    memId=1000
    
    print("--------------Member Id Check Test--------------")
    if checkMemId(memId):
        print("Member Id",memId,"is valid")
        
    else:
        print("Member Id",memId,"is not valid")


    
    print("--------------CheckOutTest--------------")
    
    try:
        dic=performCheckout(bookId,memId)
        print(database.toTableStr(dic,["Book Id","Title",
                                    "Author","Purchase Date","Member Id"]))
        print("Book with id",bookId,"is checkedout by member with id:",memId)
        
    except Exception as e:
        print(str(e))

    #rewriting the files to restore the original data
    database.writeFile("database.txt",database.toTableStrWithoutHeading(booksDic1))
    database.writeFile("logfile.txt",database.matrixToString(logs1))


if __name__=="__main__":
    test()
