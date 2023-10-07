#Author: Muhammad Hamza Sajjad
#Date:18/11/2019
#last update:11/12/2019

'''
    this module contains the functions that allow to get books from
    the database and get list of logs
    getbook titles with number of borrows associated to each title
    get all the book titles with popularity associated to each title
    generate a graph indicating the popularity of each book title 
'''

from sys import path
from os.path import abspath,dirname,join
thisDir = dirname(abspath(__file__))
path.append(thisDir)
import data.database as database

#for generating pyplot graph
from operator import itemgetter
import matplotlib.pyplot as plt
from datetime import datetime



##--------------------functions to obtain data from database--------------------

def getLogs():
    '''returns a list of lists that contains logs 
    '''
    return database.getLogData()


def getBooks():
    '''returns a dictionary of books where the key is book id and the 
    '''
    return database.getBooks()



##---------------------functions to workout the popularity---------------------

def countInLogs(logsList,bookId):
    '''the function returns how many times a bookId appears
    in log list and the last date when it was borrowed
    :param logsList contains the list of all book checkout and return operations
    :param bookId contains the bookId to be searched in the logs
    '''
    
    count=0
    lastDate="--"
    
    #the last date of a book being borrowed
    #will be it's last appearance in log file
    for log in logsList:
        
        if log[0]==bookId:
            count+=1
            lastDate=log[1]
    
    return count,lastDate



def compareDate(strDate1,strDate2):
    '''returns 0 if strDate1 equals strDate2
    1 if strDate1 is greater thanstrDate2
    and -1 otherwise
    :param strDate1 is the first date in string format
    :param strDate2 is the second date in string format
    '''
    
    if strDate1==strDate2:
        return 0
    #I have decided that if a book is never borrowed it has -- as borrow date
    #but executing strptime on "--" would create and exception so I manage it
    elif strDate2=="--":
        return 1
    
    elif strDate1=="--":
        return -1
    
    else:
        date1=datetime.strptime(strDate1,"%d/%m/%Y")
        date2=datetime.strptime(strDate2,"%d/%m/%Y")
        
        if date1>date2:
            return 1
        #case where the dates are the same is already done
        else:
            return -1
    

def countBookLogs():
    '''returns a dictionary of book titles associated to number of times
    it is borrowed, it's author, number of copies of that book,
    last date (in string format) when it was borrowed and the lowest purchase
    date among all the copies of a title
    if a book with that title was never borrowed it will have '--' as last date
    
    '''

    bookDic=database.getBooks()
    logsList=database.getLogData()
    popularTitles={}

    
    for bookId in bookDic:
        
        nOfBorrows,lastdate=countInLogs(logsList,bookId)
        title=bookDic[bookId][0]
        purDate=bookDic[bookId][2]
        
        #if I have already inserted that book title in dictionary
        if title in popularTitles:
            
            popularTitles[title][0]+=nOfBorrows
            popularTitles[title][2]+=1

            #if the last checkout date for this book copy is newer
            if compareDate(lastdate,popularTitles[title][3])==1:
                popularTitles[title][3]=lastdate

    #if the purchase date of this bookid is older than the saved purchase date
            if compareDate(popularTitles[title][4],purDate)==1:
                popularTitles[title][4]=bookDic[bookId][2]
                
        else:
            author=bookDic[bookId][1]
    #the third item in the list indicates number of copies of that book
            popularTitles[title]=[nOfBorrows,author,1,lastdate,purDate]

            
    return popularTitles



def popularBooks():
    '''returns a dictionary of book titles each of them associated to a list
    where the first element is the popularity rating**,the second is the number
    of times the book was borrowed, the third is the author's name, the fourth
    is the purchase date of the oldest book copy of that book in the library
    **rating is calculated by dividing the number of borrows by number of
    days since the first book copy of that title was purchased
    then divide it by the number of copies of the title
    '''
    
    countedTitles=countBookLogs()
    titlesPopularity={}
    
    for title in countedTitles:
        
        #calculate the popularity rating as indicated in the doc strings
        strPurDate=countedTitles[title][4]
        heldDays=(datetime.now()-datetime.strptime(strPurDate,"%d/%m/%Y")).days

        #multiplying by 100 so numbers don't remain very low
        popRating=100*countedTitles[title][0]/(heldDays+1)

        #dividing by number of copies because a book that
        #has more copies will be borrowed by more people
        #I find borrow rate per copy
        popRating=popRating/countedTitles[title][2]
        #print(title,countedTitles[title][2])
        
        titlesPopularity[title]=[popRating]+countedTitles[title]
        
    return titlesPopularity




###---------------------Functions generating the graph---------------------

def updateTooltip(bar,tooltip,details,ax):
    '''updates the tooltip by visualising it next to the bar and updating
    the details of the specific bar
    :param bar is the bar of which i want to show the details
    :param tooltip is the tooltip to be updated
    :param details is the list that contains the details of all the bars
    '''
    
    #x indicates the index of the bar which will be the same as
    #that of it's details in the list details
    x = int(bar.get_x()+bar.get_width()/2)
    y = bar.get_y()+bar.get_height()
    
    tooltip.xy = (x,y)
    
    text="Borrows: "+str(details[x][0])+"\n"+"By "+details[x][1]
    text+="\nCopies: "+str(details[x][2])
    text+="\nLast borrow: "+details[x][3]+"\nPurc. Date: "+details[x][4]
    
    tooltip.set_text(text)


def hover(event,fig,ax,bars,tooltip,details):
    '''when the user hover on the canvas containing the figure, the function
    checks whether the hover is on a specific bar and then it and then
    it updates the tooltip by show the details of that bar
    '''
    
    if event.inaxes==ax:

        #scan all the bars
        for bar in bars:

            cont,ind=bar.contains(event)
            
            #if hover is in this bar
            if cont:
                
                updateTooltip(bar,tooltip,details,ax)
                tooltip.set_visible(True)
                fig.canvas.draw_idle()
                return
    
    if tooltip.get_visible():
        
        tooltip.set_visible(False)
        fig.canvas.draw_idle()


def plotPopularity():
    """creates a bar graph using pyplot which indicates the popularity
    of each book title and returns 
    """
    
    titlesPopularity=popularBooks()
    sortedByPop = sorted(titlesPopularity.items(), key=itemgetter(1),
                         reverse=True)

    titles=[] ##will be the x axis of the bar graph
    #details: n# of borrows,author,n# Of copies, last borrow date, purchase date
    details=[] ##will be displayed in the tooltip
    rating=[]##will be used as height of the bars
    colors=["green"]*5+["cyan"]*(len(sortedByPop)-10)+["red"]*5

    for (i,j) in sortedByPop:
        titles.append(i)
        details.append(j[1:])
        rating.append(j[0])


    #---generate the bar graph and configure it---
    
    fig=plt.figure()
    ax=plt.subplot()
    
    #create bar graph and set legend if it we have more than 10 titles
    #because otherwise top 5 and worst 5 does not make sense
    
    x_labels=[i for i in range(len(titles))]
    if len(rating)>=10:
        bars1=plt.bar(x_labels[0:-5], rating[0:-5],color=colors[0:-5],
                      label="Top 5")
        bars2=plt.bar(x_labels[-5:], rating[-5:],color=colors[-5:],
                      label="Worst 5")
        bars=bars1+bars2
        
        plt.legend()
        
    else:
        bars=plt.bar(x_labels,rating,color=colors[0:len(rating)])

    
    plt.xticks(x_labels, titles,rotation=90)

    
    plt.title("Popularity graph")
    plt.ylabel("rating")

    plt.subplots_adjust(top=0.85)
    
    #configuring the tooltip
    tooltip = ax.annotate("", xy=(0,0), xytext=(-40,-20), size=7,
            textcoords="offset points",bbox=dict(boxstyle="round", fc="white",
            ec="b", lw=2))
    
    tooltip.set_visible(False)
    fig.canvas.mpl_connect("motion_notify_event",lambda event: hover(event,fig,
                                                    ax,bars,tooltip,details))
    plt.tight_layout()

    #returning all those elements because they may be needed for embedding
    visualisationData=[plt,fig,ax,bars,tooltip,details]
    
    return visualisationData
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          



def test():
    '''function applies test on all of the functions of this modules booklist
    and shows their result on comand line
    '''
    
    books=getBooks()
    logs=getLogs()
    dic=countBookLogs()
    headings=["Title","number of Borrows","Author",
              "copies","lastDate","purDate"]
    print("-------Book titles with number of borrows-------")
    print(database.toTableStr(dic,headings))
    print("-------Book titles with popularity Rating-------")
    print(database.toTableStr(popularBooks(),
                              [headings[0]]+["rating"]+headings[1:]))
    print("-------Datescomparing-------")
    print(compareDate("10/12/2019","--"))
    input("press enter to view graph...")
    plt=plotPopularity()[0]
    
    plt.show()
    
    bookId1=logs[0][0]
    nBorrows,lastDate=countInLogs(logs,bookId1)
    print("book with Id "+str(bookId1)+" was borrowed "+str(nBorrows)+" times.")
    

if __name__=="__main__":
    test()
    
