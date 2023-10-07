#Author: Muhammad Hamza Sajjad
#Date: 20/11/2019
#lastupdate:11/12/2019


"""
    This module contains functions used to search books
    matching specific parameters (eg. title)
"""

from sys import path
from os.path import abspath,dirname,join

thisDir1 = dirname(abspath(__file__))
path.append(join(thisDir1,"data"))
import database


def searchTitles(bookTitle):
    """The function takes the dictionary containing books as parameter
    and returns a list of books that matching the title
    """
    
    bookDic=database.getBooks()
    foundTitles=[]

    #ignoring the extra spaces
    bookTitle=str(bookTitle).strip()
    bookTitle=bookTitle.lower()
    
    for bId in bookDic:
        
        if bookDic[bId][0].lower().__contains__(bookTitle):
            
            if bookDic[bId][0] not in foundTitles:
                
                foundTitles.append(bookDic[bId][0])
                
    return foundTitles

def matchesAny(bookData,searchvalue):
    """the function returns true if the searchValue matches any of
    the elements of the list bookData
    :param bookData: is the list that is to be matched with the searchvalue
    :param searchvalue: is the value to be searched in the list bookData
    """
    for fields in bookData:
        if searchvalue in str(fields).lower():
            return True
        
    return False

def matches(bookData,searchvalue,onlySecond=True):
    """the function returns true if the searchvalue matches
    any or only second element of the list bookData depending on the
    value of onlySecond
    :param bookData: is the list of values to searchvalue may be matched
    :param searchvalue: is the value to be matched with the items of the list
    :param onlySecond: set to True if want to match with only second element
    false if want to match with any element
    """
    
    if onlySecond:
        
        return searchvalue in str(bookData[1]).lower()
    
    else:
        
        return matchesAny(bookData,searchvalue)
        

def searchBook(searchKey,onlyByTitle=True):
    """The function returns a dictionary of books of which the title or
    any other fields of the book (depends on the value of onlyByTitle) match
    the searchKey. The available books will be at the top of the dictionary
    :param bookTitle: is the 
    :param onlyByTitle: indicates if you want to match only the title
    """

    bookDict=database.getBooks()
    
    #ignoring the extra spaces and converting to lowercase
    searchKey=str(searchKey).strip()
    searchKey=searchKey.lower()
    
    rtnBooks={}
    for bId in bookDict:
        
        if matches([bId]+bookDict[bId],searchKey,onlyByTitle):
            
            if bookDict[bId][3]!=0:
                #appending the matching book at the end if it is borrowed
                rtnBooks[bId]=bookDict[bId]
                
            else:
                #'appending' the matching book at the top if it is available
                tempDic={bId:bookDict[bId]}
                tempDic.update(rtnBooks)
                rtnBooks=tempDic
                
    return rtnBooks

def test():
    """The function test all the functions in the module booksearch
    and prints their result on command line
    """
    
    title="hArr"
    print("books matching word "+str(title)+" in their title")
    booksDic=database.getBooks()
    
    print(database.toTableStr(searchBook(title),
          ["BookId","Title","Author","Purchase Date","Member Id"]))
    
    print("list of titles matching word "+str(title))
    print("\n".join(searchTitles(title)))


if __name__=="__main__":
    test()
