#Author: Muhammad Hamza Sajjad
#Date: 4/12/2019
#lastupdate: 11/12/2019
#version 2.0 of GUI

#in case you are wondering where is the first version of the GUI
#IT WAS DISAPPROVED!!!


"""
    this module contains functions used to implement
    the graphical user interface for the librarian
    it lets the user execute all the functionalities
    implemented in booksearch, booklist, bookcheckout and bookreturn
"""

#-->>NOTE: whenever I am declaring global varibale in a function
#it means that they will be used outside of that function within another one


from sys import path
from libraryOperations import bookcheckout,bookreturn,booklist,booksearch
from tkinter.ttk import Treeview,Scrollbar
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


selectedOpt=None
tableGroup=None

#is the id of the after event that resets the status bar
resetId=None

menufont=("Arial Rounded MT Bold",11)
genfont=("calibri",11)

menucolor="#0079bf"
menuhovercolor="#298fca"

currentBookId=""

def init():
    """The function initializes the window, creates the menu,
    the option Frame, status bar and shows the welcome message
    """
    #I declare these variables as global so they will be accessable
    #in the other functions.
    global mainFrame,optFrame,statusLbl,statusVar,statusLbl

    #This frame contains all of the widgets of the window
    mainFrame=tk.Frame(win)
    mainFrame.pack(fill="both",expand=1)
    mainFrame["background"]="#5ba4cf"

    #creating menu
    menuF=tk.Frame(mainFrame)
    menuF.pack(side="top",fill="x")
    createmenu(menuF)

    #option frame contains the widgets of the selected option from menu
    optFrame=tk.Frame(mainFrame,padx=10)
    optFrame.pack(fill="both",expand=1)
    optFrame["background"]=mainFrame["background"]

    #message displayed only at the start
    welcomeVar=tk.StringVar()
    welcomeVar.set("")
    tk.Label(optFrame,textvar=welcomeVar,bg=optFrame["background"],fg="Blue",
             font=("Algerian",11)).pack(fill="both",expand=1)
    
    win.after(1000,setVar,welcomeVar,"Welcome")
    msg="Please select an option from the menu above"
    win.after(4000,setVar,welcomeVar,msg)

    #creating status bar and configuring it
    statusVar=tk.StringVar()
    statusLbl = tk.Label(mainFrame, text="on the way…", bd=1, relief="sunken",
                         anchor="w",textvariable=statusVar)
    
    statusLbl.pack(side="bottom",fill="x",pady=(0,0))
    msg="WELCOME to library management system"
    win.after(500,upgradeStatus,msg,"green")
    statusLbl.config(font=("Courier",12))
    
    resizeIfRequired()


#--------------------------general GUI functions--------------------------


def setVar(var,value):
    """The function sets the value of the tkinter variable
    :param var: is tkinter variable
    :param value: is the value to be changed
    """
    var.set(value)

def changeWidgetColor(widget,color):
    """The function changes background colour of a widget
    :param widget: is the widget of which you want to change the background
    :param color: is the background color in string format
    """
    
    try:
        widget["background"]=color
    except:
        pass

def resizeIfRequired():
    """the function checks if the size of the window is big enough
    to hold all the widgets and resizes it if required
    """
    win.update()

    #required height and width
    reqw=mainFrame.winfo_reqwidth()
    reqh=mainFrame.winfo_reqheight()

    #setting width and/or height if they are less than the required ones
    if mainFrame.winfo_width()<reqw:
        win.geometry(str(reqw)+"x"+str(win.winfo_height()))
        win.update()
        
    if mainFrame.winfo_height()<reqh:
        win.geometry(str(mainFrame.winfo_width())+"x"+str(reqh))
        win.update()

    win.minsize(width=0,height=reqh)

def clearContainer(container):
    """deletes all the widgets contained in the container
    :param container: is the container to be cleared
    """
    
    for widget in container.winfo_children():
        widget.destroy()

def upgradeStatus(msg,bgcolor="red"):
    """changes the text of the status bar to message
    and sets the background color
    :param msg: is the string to be displayed
    :param bgcolor: is the new background colour
    """
    global resetId
    #cancelling after event which would reset status earlier
    if resetId is not None:
        win.after_cancel(resetId)
        
    if statusLbl.winfo_exists()==1:
        
        statusVar.set(str(msg))
        statusLbl.config(bg=bgcolor,fg="white")
        resetId=win.after(3000,reset_status)

def reset_status():
    """Resets the text of the status bar
    """
    if statusLbl in mainFrame.winfo_children():
        
        statusVar.set("STATUS BAR")
        statusLbl.config(bg=menucolor,fg="black")


def alignInCenter(window,winW,winH):
    """Aligns the window in the center of the screen
    :param window: is the window
    :param winW: is the width of the window
    :param winH: is the height of the window
    """
    screenW = window.winfo_screenwidth()
    screenH = window.winfo_screenheight()
    # calculat window x, y position on screen
    x = (screenW/2) - (winW/2) - 100
    y = (screenH/2) - (winH/2) - 100
    window.geometry('%dx%d+%d+%d' % (winW, winH, x, y))


#--------------------------menu related functions--------------------------

def on_opt_enter(event):
    """when user hovers on menu option the function
    sets the background of the option hovered
    """
    
    if event.widget!=selectedOpt:
        event.widget['background'] = menuhovercolor


def on_opt_leave(e):
    """when the hover is left the background color is reset
    """
    if e.widget!=selectedOpt:
        e.widget['background'] = menucolor


def createmenubutton(frame,label):
    """creates a menu button and returns it
    """
    
    button=tk.Button(frame,text=label,bg=menucolor,borderwidth=0,
                     height=2,font=menufont)
    button.pack(side="left",fill="both",expand=1)

    #managing color changing feature on hover
    button.bind("<Enter>", on_opt_enter)
    button.bind("<Leave>", on_opt_leave)
    
    return button


def createmenu(menuF):
    """Creates all the menu options with their color and click events
    """
    global searchOpt,checkoutOpt,returnOpt,popularityOpt
    
    searchOpt=createmenubutton(menuF,"Search Book")
    searchOpt.bind("<ButtonRelease-1>",search_opt_clicked)
    
    checkoutOpt=createmenubutton(menuF,"Checkout Book")
    checkoutOpt.bind("<ButtonRelease-1>",checkout_opt_clicked)
    
    returnOpt=createmenubutton(menuF,"Return book")
    returnOpt.bind("<ButtonRelease-1>",return_opt_clicked)
    
    popularityOpt=createmenubutton(menuF,"Books popularity")
    popularityOpt.bind("<ButtonRelease-1>",popularity_opt_clicked)
    

def menuOptChanged(newOpt):
    """the function changes the background color of new menu Option
    and reset that of the old one
    :param newOpt: is the new menu option that has been selected
    """
    global selectedOpt
    
    if selectedOpt is not None:
        selectedOpt["background"]=menucolor
        
    selectedOpt=newOpt
    newOpt["background"]=mainFrame["background"]


#--------------------------search related functions--------------------------


def search_opt_clicked(e):
    """the function shows the the search bar and binds the required event on it
    """
    global searchText,onlyTitle
    
    if selectedOpt!=searchOpt:
        #menu option is changed so clear the frame that contains related widgets
        menuOptChanged(searchOpt)
        clearContainer(optFrame)

        fr=tk.Frame(optFrame,bg=optFrame["background"])
        fr.pack(fill="x",padx=(20,10),pady=(20,10))

        
        searchText=tk.Entry(fr,font=(genfont[0],12))
        searchText.pack(padx=10,ipady=1,side="left",fill="both",expand=1)
        searchText.bind("<KeyRelease>",search_text_edited)

        #checkbox that allows to search only in title or in any field
        onlyTitle=tk.IntVar()
        chkSearch=tk.Checkbutton(fr,text="match title only",variable=onlyTitle)
        chkSearch.pack(side="left")
        chkSearch.config(bg=optFrame["background"])
        onlyTitle.set(1)
        
        resizeIfRequired()
        
    searchText.focus()
    msg="Please type a key in the search bar"
    win.after(700,upgradeStatus,msg,"green")
    


def search_text_edited(e):
    global tableGroup

    #if table is not created yet or it exists but
    #is not in option frame the create it
    if tableGroup is None or tableGroup not in optFrame.winfo_children():
        createTable(optFrame)
        resizeIfRequired()
        
        msg="Did you know that you can click on table heading to sort"
        win.after(100,upgradeStatus,msg,"green")
        
    title=e.widget.get()
    loadTable(booksearch.searchBook(title,onlyTitle.get()))

#~~~~~~~~~~~~~~~table related functions~~~~~~~~~~~~~~~


def treeview_sort_column(tv, col, reverse):
    """The function is used to sort a certains column of the table tv
    when the user clicks on it 
    """
    l = [(tv.set(k, col), k) for k in tv.get_children('')]

    #if the values of the column are integers then sort by integer values
    #otherwise sort string values    
    try:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)
    except:
        l.sort(key=lambda t: t[0], reverse=reverse)
        

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    #overwriting the event so that the next time the sort order changes
    #from ascending to descending and viceversa 
    tv.heading(col,
               command=lambda: treeview_sort_column(tv, col, not reverse))


def createTable(container):
    global treeTable,tableGroup

    tk.Label(container,text="Books Table",bg=container["background"],
             font=(genfont[0],16)).pack(padx=10)

    #creating table container and setting table headings
    tableGroup = tk.Frame(container,bg=container["background"])
    tableGroup.pack(fill="both",expand=1,pady=(3,10),padx=10)
    
    cols = ['BOOK ID', 'TITLE', 'AUTHOR','PURCHASE DATE',"MEMBER ID"]
    
    treeTable = Treeview(tableGroup, columns=cols, show='headings'
                             ,selectmode="browse")

    #adding vertical scroll bar to the table
    vsb = Scrollbar(tableGroup, orient="vertical", command=treeTable.yview)
    vsb.pack(side="right",fill="y")
    
    treeTable.configure(yscrollcommand=vsb.set)
    
    # set column headings and their width
    for col in cols:
        treeTable.heading(col, text=col,command=lambda c=col:
                          treeview_sort_column(treeTable, c, False))
        treeTable.column(col, width=130)

    treeTable.pack(side="left",fill="both",expand=1)
    treeTable.bind("<<TreeviewSelect>>",on_table_select)


def clearTable():
    """the functions clears the treeTable by removing all records
    """
    for i in treeTable.get_children():
        treeTable.delete(i)


def loadTable(dic):
    """puts the values of the dictionary dic in the table
    the key will be the first element
    """
    clearTable()
    
    for bookId in dic:
        treeTable.insert("","end",values=[bookId]+dic[bookId])


def on_table_select(event):
    """Saves the selected book id in the global varibale so
    it can be used for checkout or return
    """
    global currentBookId
    currentBookId=str(treeTable.item(treeTable.selection()[0])["values"][0])


#--------------------------Checkout related functions--------------------------

def checkout_opt_clicked(e):
    """the function clers the option frame and creates a 
    """
    
    global bookIdText,memIdText,checkoutBtn
    
    menuOptChanged(checkoutOpt)
    clearContainer(optFrame)

    #frame that contains the checkout widgets
    fr=tk.Frame(optFrame,pady=20,padx=30,bg=optFrame["background"])
    fr.pack(side="top",fill="x")
    fr.columnconfigure(1,weight=1)

    #creating labels and entry boxes for checkout
    tk.Label(fr,text="Book Id",bg=optFrame["background"]).grid(row=0,column=0)
    bookIdText=tk.Entry(fr,font=genfont)
    bookIdText.insert("end",currentBookId)
    bookIdText.grid(row=0,ipady=1,column=1,sticky="ew")
    bookIdText.focus()
    
    tk.Label(fr,text="Member Id",bg=optFrame["background"]).grid(row=1,column=0)
    memIdText=tk.Entry(fr,font=genfont)
    memIdText.grid(row=1,ipady=1,column=1,sticky="ew",pady=20)
    memIdText.bind("<Return>",on_checkoutBtn_click)

    #checkout button
    checkoutBtn=tk.Button(fr,text="Perform Checkout",font=genfont,
                          command=on_checkoutBtn_click)
    checkoutBtn.grid(row=2,column=0,columnspan=2,sticky="ew")
    
    msg="Insert book Id and member Id to perform checkout"
    win.after(700,upgradeStatus,msg,"green")
    resizeIfRequired()
    
def on_checkoutBtn_click(e=None):
    """The functions is executed when the user wishes to perform checkout
    performs checkout if the bookId and memberid are valid and the book is
    available
    """

    #if user does not insert any value
    if bookIdText.get()=="":
        upgradeStatus("Please insert a book id")
        bookIdText.focus()
        
    elif memIdText.get()=="":
        upgradeStatus("Please insert a member id")
        memIdText.focus()

    #if the memberid or the bookid are not numbers display error
    elif not bookIdText.get().strip().isdigit() or not (
        memIdText.get().strip().isdigit()):
        upgradeStatus("Book id and member id must be numbers")
        
    else:
        try:
            bookId=int(bookIdText.get())
            memId=int(memIdText.get())
            dic=bookcheckout.performCheckout(bookId,memId)

        #the checkout is done successfully so the checkout button becomes green
            win.after(100,changeWidgetColor,checkoutBtn,"green")
            win.after(2100,changeWidgetColor,checkoutBtn,"SystemButtonFace")
            
            upgradeStatus("Checkout Done Successfully","green")
            
        except Exception as ex:
            #there is an error so button becomes red and status shows error
            win.after(10,changeWidgetColor,checkoutBtn,"red")
            win.after(2100,changeWidgetColor,checkoutBtn,"SystemButtonFace")
            
            upgradeStatus(ex)



#--------------------------Book return related functions--------------------------

def return_opt_clicked(e):
    """The function is executed when the return book option is selected
    it creates the widgets required to return a book
    """
    global bookIdText,returnBtn
    
    menuOptChanged(returnOpt)
    clearContainer(optFrame)

    #frame that contains the widgets required to return a book
    fr=tk.Frame(optFrame,pady=20,padx=30,bg=optFrame["background"])
    fr.pack(side="top",fill="x")
    fr.columnconfigure(1,weight=1)

    #the label, entry and button required to returna a book
    tk.Label(fr,text="Book Id",padx=10,
             bg=optFrame["background"]).grid(row=0,column=0,sticky="ew")
    bookIdText=tk.Entry(fr,font=genfont)
    bookIdText.grid(row=0,ipady=1,column=1,sticky="ew")
    bookIdText.focus()
    bookIdText.bind("<Return>",on_returnBtn_clicked)
    bookIdText.insert("end",currentBookId)
    
    returnBtn=tk.Button(fr,text="Return Book",
                        font=genfont,command=on_returnBtn_clicked)
    returnBtn.grid(row=2,column=0,columnspan=2,sticky="ew",pady=(20,0))

    
    resizeIfRequired()
    msg="Insert the Id of the book to be returned"
    win.after(700,upgradeStatus,msg,"green")

def on_returnBtn_clicked(e=None):
    """The functions is used to return a book when user clicks on return button
    the functions displays error bookId is not valid or was never checkedout
    """

    #if no book id is provided or bookid is not a number show error message
    if bookIdText.get()=="":
        
        bookIdText.focus()
        upgradeStatus("Please insert a book id")
    elif not bookIdText.get().strip().isdigit():
        upgradeStatus("Book id must be a number")
    else:
        try:
            bookId=int(bookIdText.get())
            dic=bookreturn.returnBook(bookId)

            #book is returned successfully so turn the button green for 1.9 secs
            win.after(100,changeWidgetColor,returnBtn,"green")
            win.after(2000,changeWidgetColor,returnBtn,"SystemButtonFace")
            
            upgradeStatus("Book Returned Successfully","green")
            
        except Exception as ex:
            win.after(100,changeWidgetColor,returnBtn,"red")
            win.after(2000,changeWidgetColor,returnBtn,"SystemButtonFace")
            
            upgradeStatus(ex)


#--------------------------Popularity graph related functions--------------------------
   
def popularity_opt_clicked(e):
    """executed when the popularity options is selected from the menu
    generates the popularity graph, embedds it in tkinter and displays it
    """
    menuOptChanged(popularityOpt)
    clearContainer(optFrame)

    optFrame.config(padx=0)
    visualizeByPopularity(optFrame)
    
    resizeIfRequired()
    msg="You can hover on bars for more details"
    win.after(300,upgradeStatus,msg,"green")



def visualizeByPopularity(container):
    '''
    the function generates a graph representing the popularity
    of each book title and embedds it in tkinter container.
    the function activates the hover functionality over the graph
    '''
    global canvas
    plotItems=booklist.plotPopularity()
    plt,fig,ax,bars,tooltip,details=plotItems
    fig.patch.set_facecolor(mainFrame["background"])
    
    container.config(padx=0)

    #creting tkinter canvas and embedding figure in it
    canvas=FigureCanvasTkAgg(fig,master=container)
    canvas.get_tk_widget().configure(background='black', highlightcolor='black',
                                     highlightbackground='black')
    canvas.draw()
    
    canvas.get_tk_widget().pack(fill="both",expand=1)
    toolbar=NavigationToolbar2Tk(fig.canvas,container)
    toolbar.update()

    #manage the hover event
    fig.canvas.mpl_connect("motion_notify_event",lambda event:
                           booklist.hover(event,fig,ax,bars,tooltip,details))
    
    fig.canvas.draw()



#---------------End of all functions---------------


win=tk.Tk()
win.title("Library")

init()

alignInCenter(win,500,200)

win.focus_force()
win.mainloop()

