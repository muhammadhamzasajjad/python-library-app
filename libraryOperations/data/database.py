#Author: Muhammad Hamza Sajjad
#creation date: 16/11/2019
#last update:07/12/2019

"""
    this module contains functions to do read,
    write and append operations on file
    to get checkout logs, get books from the database
    contains also functions to convert a dictionary to
    a table String and a nestedList to string
    it will only read/write files that are in the same direcotry as it
"""

import datetime
from os.path import abspath,dirname,join
thisDir = dirname(abspath(__file__))



#----------------------File operations----------------------

def readfile(fname):
    """returns a list of strings containing each line contained in the file
    :param fname: the name of file contained in the directory of this file
    :return string representation of the dictinary:
    """

    #join the directory of this module to the fname
    f=open(join(thisDir,fname), "r")
    content=f.readlines()
    f.close()

    return content



def writeFile(fname,string):
    """rewrites the given file with fname with the given string
    :param fname indicates the name of file which must be
    in the same directory of this module
    :param string is the string to be written in the file
    """
    
    f=open(join(thisDir,fname),"w")
    f.write(string)
    f.close()


#----------------------Frome file in data structure----------------------

def appendline(fname,line):
    """appends line in the fname file in the same directory of this module
    :param fname is the name of file
    :param line is the line to be appended
    """
    
    f=open(join(thisDir,fname),"a")
    f.write(line+"\n")
    f.close()
    


def getBooks():
    """the function opens the database.txt file and returns a
    dictionary containing the books details, the key is the book id
    """
    
    booksInLines=readfile("database.txt")
    
    dic={}
    
    for i in booksInLines:
        
        #if a row does not respect the expected formate the program will
        #ignore that row.
        #imagine if the user changes the values of the file
        try:
            
            #seperating fields of each line and saving them
            bookstr=i.split("|")
            
            bookid=int(bookstr[0].strip())
            title=bookstr[1].strip()
            author=bookstr[2].strip()
            purDate=bookstr[3].strip()
            memId=int(bookstr[4].strip())
            
            dic[bookid]=[title,author,purDate,memId]
            
        except:
            pass


    return dic



def getLogData():
    """The function returns a list of list containing all the logs
    each sublist contains bookId,borrowDate,returnDate. Note that if a
    book is still borrowed an not returned yet it will have -- as return DAte
    """
    
    lines=readfile("logfile.txt")
    logs=[]

    #scan all lines
    for line in lines:
        
        try:
            #separate the fields
            fields=line.split(";")
            
            bookId=int(fields[0].strip())
            checkoutDate=fields[1].strip()
            returnDate=fields[2].strip()
            #append them in the list
            logs.append([bookId,checkoutDate,returnDate])
            
        except:
            pass

    return logs



###----------------------Additional functions for printing----------------------


def listToString(List):
    """converts the list into a string where each list item is seperated by ';'
    :param List is the list to be converted in string
    """
    
    rtnStr=""
    
    for item in List:
        rtnStr+=str(item)+";"

    #ignoring the last ;
    return rtnStr[0:-1]


def matrixToString(nestedList):
    """
    converts a matrix (a nested list) in a string where each
    list is separated by '\n' and each
    element of the sublist is separated by ';' a
    """
    
    matrixInStr=""
    
    for l in nestedList:        
        matrixInStr+=listToString(l)+"\n"

    return matrixInStr


def maxLenColumn(dic,col):
    """
    returns the maximum length of a given column in the dictionary
    :param dic is the dictionary
    :param col is the column index
    """
    
    maxl=0
    
    for i in dic:
        maxl=max(maxl,len(str(dic[i][col])))
        
    return maxl



def getTableCell(elem, cellWidth):
    """
    returns a table cell of cellWidth in string format containing the element
    :param elem is the element to be represented in the cell
    :param cellWidth is the width of the table cell
    """
    
    elemStr=str(elem)
    
    return elemStr+" "*(cellWidth - len(elemStr))+"  |"



def getTableRow(rowList, columnWidth):
    """takes a list and return the a row of the table where
    each element of the rowList is represented as a table cell
    :param rowList: is the list to be converted in table row
    :param columnWidth:
    """
    
    strRow=""
    
    for i in range(len(rowList)):
        strRow+=getTableCell(rowList[i], columnWidth[i])
    
    return strRow



def toTableStr(dic, tHeading):
    """the function returns a table (with heading) in string format containing
     elements of the dictionary
    :param dic the dictionary to be represented:
    :param tHeading tableHeading:
    :return string representation of the dictinary:
    """
    
    maxColumnLen=[]
    keys=dic.keys()

    #find the maximum for the first column (the keys of dictionary)
    maxColumnLen.append(max(len(tHeading[0]),
                    len(max([str(i) for i in keys]+[""],key=len))))

    
    for i in range(1, len(tHeading)):
        maxColumnLen.append(max(len(tHeading[i]), maxLenColumn(dic, i - 1)))

        
    table2= getTableRow(tHeading, maxColumnLen) + "\n"

    #get each row of table cells with maximum 
    for i in dic:
        table2+=getTableRow([i]+dic[i],maxColumnLen)+"\n"

    
    return table2



#I have both the functions because this way
#if I need to print table without heading on screen I can use the function
#with heading
def toTableStrWithoutHeading(dic):
    """The function returns a table (without heading) in string containing
    elements of the dictionary
    :param dic:
    :return:
    """
    
    firstkey=list(dic.keys())[0]
    strTabelWithHeading=toTableStr(dic,[" "]*(len(dic[firstkey])+1))

    #ignoring the heading
    return "\n".join(strTabelWithHeading.split("\n")[1:]) 



#----------------------Testing function----------------------

def test():
    """
    tests each function and prints their result on command line
    """
    print("---------------toTableStrWithoutHeading() test---------------")
    print(toTableStrWithoutHeading({1:["field1","w2"],2:["hello","good morning"]
                                    }))
    print("---------------readfile() test---------------")
    print("reading file database.txt...")
    print(readfile("database.txt"))
    print("\n\n\nfetching available books...")
    booksDic=getBooks()
    
    print("---------------toTableStr() test---------------")
    print("\n~~~~Please widen your screen to be able to see the table "\
          "correctly~~~~")
    print(toTableStr(booksDic,["book ID","Title","Author","Purchase Date",
                               "member ID"]))
    print("\n\n\nReading log file")
    log=getLogData()
    
    print("---------------listToString() test---------------")
    print(listToString(log[0]))
    
    print("---------------matrixToString() test---------------")
    ##saving all log lines except from the last one which will be appended later   
    logStr=matrixToString(log[0:-1])
    print(logStr)
    print("\n\n\nwriting logfile.txt file")
    writeFile("logfile.txt",logStr)

    ##appendin the last log line to maintain the original data
    print("\n\n\nappending logfile.txt file")
    appendline("logfile.txt",listToString(log[-1]))
    
    print("---------------maxLenColumn() test---------------")
    print("max length of column",0,"is ",maxLenColumn(booksDic,0))
    
    print("---------------getTableCell() test---------------")
    cell1=getTableCell("cell1",7)
    cell2=getTableCell("cell2",10)
    print("Tow table cells combined \n"+cell1+cell2)
    
    print("---------------getTableRow() test---------------")
    print(getTableRow(["rc1","rc2","rc3"],[5,5,6]))

if __name__=="__main__":
    test()
