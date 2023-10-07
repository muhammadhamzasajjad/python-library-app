#Author: Muhammad Hamza Sajjad
#Date: 20/11/2019
#lastupdate:08/12/2019


"""
    this module contains functions used to return a book with a given id.
    if from the logfile it appears that the book was checkedout then we
    can return the book and the return date will be today's date
    as it happens in the real life.
"""

from sys import path
from os.path import abspath,dirname,join
thisDir = dirname(abspath(__file__))
path.append(join(thisDir,"data"))
import database
from datetime import datetime


def indexInColumn(item,columnIndex,nestedList):
    '''returns the highest row index of the nestedList where we find the item
    returns -1 if the item does not appear 
    :param item: is the item to be searched
    :param nestedList: is the list where to search the item
    :param columnIndex: is the columnIndex of the nestedList where the item
    should appear
    '''
    
    index=-1
    
    for i in range(len(nestedList)):
        
        if item==nestedList[i][columnIndex]:
            
            index= i
    
    return index


def returnBook(bookId):
    """The function performs the book return operaion of a given book
    raises exceptions the book to be returned was never borrowed or
    is not saved in the records
    :param bookId: is the id of the book to be returned
    """
    
    bookDic=database.getBooks()
    checkoutLogs=database.getLogData()
    indexInLogs=indexInColumn(bookId,0,checkoutLogs)
    
    if bookId not in bookDic:
        
        raise Exception("Book id "+str(bookId)+" not found")
    
    #book not borrowed
    elif bookDic[bookId][3]==0:
        
        raise Exception("The book "+str(bookId)+" is not borrowed by anyone")
    
    elif indexInLogs==-1 or checkoutLogs[indexInLogs][2]!="--":
        #the book is not in checkoutlogs or it has been returned but someone
        #messed up with database.txt file and put a member's id
        
        bookDic[bookId][3]=0
        bookTable=database.toTableStrWithoutHeading(bookDic)
        database.writeFile("database.txt",bookTable)
        
        raise Exception("The book was not borrowed by any member")
        
    else:
        todayDateStr=datetime.now().strftime("%d/%m/%Y")
        checkoutLogs[indexInLogs][2]=todayDateStr
        database.writeFile("logfile.txt",database.matrixToString(
            checkoutLogs))
        
        bookDic[bookId][3]=0
        bookTable=database.toTableStrWithoutHeading(bookDic)
        database.writeFile("database.txt",bookTable)
        
    return bookDic

def test():
    """The function tests all of the function in this module('bookreturn') and
    displays the results on Command line
    """
    try:
        booksDic=database.getBooks()
        logs=database.getLogData()
        bookId=list(booksDic.keys())[0]
        
        indexInLogs=indexInColumn(bookId,0,logs)
        
        if indexInLogs==-1:
            print(bookId,"was never borrowed by anyone")
            
        else:
            print(bookId,"appears at line",indexInLogs+1,"in log file")
            
        returnBook(bookId)
        print("Book with id",bookId,"returned successfully")
        
    except Exception as e:
        print(e)
        
    print(database.toTableStrWithoutHeading(database.getBooks()))
    
    #restoring the original data
    bookstoStr=database.toTableStrWithoutHeading(booksDic)
    database.writeFile("database.txt",bookstoStr)
    database.writeFile("logfile.txt",database.matrixToString(logs))

if __name__=="__main__":
    test()




