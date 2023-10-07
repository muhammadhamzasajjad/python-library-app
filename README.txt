
Author:Muhammad Hamza Sajjad
Date: 11/12/2019

-----------------------GUI Related-----------------------

when the table is displayed you can sort the table by any field by clicking on it's heading
~~~~~~~The status bar~~~~~~
the status bar is displayed at the bottom of the window and is very important
because it displays all the communication messages and some features that you might not
notice at first look. So try to keep an eye on it.
When displaying a message it automatically changes it's color so it is quite noticeable.


~~~~~~bar graph~~~~~~
you will see that the bar graph is showing all of the book titles in the database
and you might wonder that it would be better if the software showed only top 10 or 
bottom 10 of the titles. But the problem is that it would never give a general idea
of tha popularity to the librarian. And if you have a closer look at the options
available at the bottom of my graph you will see that you can zoom in a certain area
to concentrate on only the first ten last ten or any interval that you like.
So you have the overview and you can concentrate on any specific range.
How does that sound?

-----------------------Books popularity-----------------------
the popularity of a book is calculated by finding the lowest purchase date among all the
copies of a book title and dividing the number of borrows of each title (i.e. the sum of 
number of borrows of each copy of that title) by number of date since the first purchase date
this number is divided by the number of copies of that title. Because a title with 100 copies
has more chances of being borrowed than that with 10. So in a way I find per copy borrow rate 
of each title.

The popularity graph contains some extra buttons at the bottom which you can use to zoom
on a certain range of title (eg. if there are hundreds of titles it might be handy to be able to
concentrate on a certain range). Save button will let you keep record of popularity if you want to.

-----------------------additional functionalities-----------------------
database.py
Additional functions are implemented to save the book related data in a well formatted table

booklist.py
Apart from the graph I have impelemented a hover function which shows the related data of a book title
when the user hovers on the bar

booksearch.py
the function searchbook is very flexible
by default the function the function searches only for the books of which the title matches the searchKey
but it gives the possibility to return all of the books of which any of the fields matches the searchKey
this functionality could be very useful eg.(search all the books purchased in 2018, or find all the books
borrowed by the member with id 4567)

menu.py
the books table is sortable.
if the user clicks on a table heading the table if sorted
there are many additional features not specified in the coursework
such as staus bar, the interactive window, the menu with hover


-------closing remarks-------
In the end if you want to know which part I am proud of
My answer is: EVERYTHING!!!
because there is a lot of effort and planning behind each of the features
