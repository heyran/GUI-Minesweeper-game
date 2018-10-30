from tkinter import *
from functools import partial
import random


def get_neighbors(count, x, y):
        ''' Return cells that are around of input cell(cells[count])'''
                
        L = [count-y-1, count-y, count-y+1, count-1, count+1,
                                count+y-1, count+y, count+y+1]
        
        # list of cells that placed in first row 
        up = []
        # list of cells that placed in last row
        down = []
        
        for i in range(x):
            up.append(y*i) 
            down.append(y*(i+1)-1)
            
        # delete numbers that are out of range
        counter = 0
        while True:
            if L[counter] < 0 or L[counter] > x*y-1:
                del L[counter]
                counter -= 1
            counter += 1
            if counter == len(L):
                break

                        
        if count in up:
            for char in L:
                if char in down:
                    L.remove(char)
            
           
        if count in down:
            for char in L:
                if char in up:
                    L.remove(char)
            
        
        return L

                
        
def end():
        ''' Show a window when game finish, either win or lose. '''
        
        end = Toplevel()
        end.geometry('100x100')

        message = Label(end, text='The End!', justify=CENTER)
        message.pack()

        # a button for closing the game window at the end 
        back_btn = Button(end, width=5, text='back', 
                          command=lambda:[end.destroy(), root.destroy()])
        back_btn.place(x=42.5, y=40)
        

def Mine(n, x, y):
        ''' When a mine cell clicked, background color of it become red and
        show other mine cells that not been sweeped.
        If a cell has been sweeped incorrectly, show with a red cross symbol.
        And game finish. '''
        
        bname = b[n]
        bname.configure(text='\u26AB', fg='black', bg='red', relief=SUNKEN)                        
        cells[n] = None
        
        for i in range(x*y):

                bname = b[i]
                
                if cells[i] == '@':
                        bname.configure(text='\u26AB', fg='black', bg='powder blue', relief=SUNKEN)                           
                else:
                        if flag[i] == '1':
                                bname.configure(text='\u26CC', fg='red', bg='powder blue', relief=SUNKEN)
                                
        end()
        


            
def num_cell(n):
                
        bname = b[n]
        bname.config(text=cells[n], bg='powder blue', fg='black')
        bname.config(relief=SUNKEN)
        cells[n] = None
        flag[n] = 1
        
        counter = 0
        for char in cells:
            if type(char) is int:
                counter += 1
                
        # finish game if all cell that haven't mine, is clicked.      
        if counter == 0 and '*' not in cells:
                end()
        
        

def empty_cell(n, width, height):
        
        bname = b[n]
        bname.config(bg='powder blue', relief=SUNKEN)
        cells[n] = None
        flag[n] = 1
        
        U = [n]
        
        while U != []:
                y = []
                
                for i in U:
                        nei = get_neighbors(i, width, height)
                        
                        for g in nei:
                                x = []
                                
                                if cells[g] != None and flag[g] == 0:

                                        bname = b[g]
                                        
                                        if type(cells[g]) is int:
                                                
                                                bname.config(text=cells[g], bg='powder blue',
                                                             relief=SUNKEN)
                                                cells[g] = None
                                                flag[g] = 1
                                                
                                        if cells[g] == '*':
                                                
                                                bname.config(bg='powder blue', relief=SUNKEN)
                                                x.append(g)
                                                cells[g] = None
                                                flag[g] = 1
                                
                                if x != []:
                                        y += x
                        
                U = y
                
        counter = 0
        for char in cells:
                if type(char) is int:
                        counter += 1
                        
        if counter == 0 and '*' not in cells:
                end()



def right_click(count, event):

        bname = b[count]
        
        if flag[count] == '1':
                bname.config(text='')
                flag[count] = 0
                
        elif flag[count] == 0:
                bname.config(text='\u26F3', fg='red')
                flag[count] = '1'
                
        
        s = 0
        for i in range(len(cells)):
                if cells[i] == '@' and flag[i] != '1':
                        break
                if cells[i] == '@' and flag[i] == '1':
                        s += 1

        num_of_mines = cells.count('@')
        if s == num_of_mines:
                end()
        
                        
                

                                        
def left_click(count, width, height, event):

        if flag[count] == 0:
                if cells[count] == '*':
                        bname = b[count] 
                        bname.config(command=partial(empty_cell, count, width, height))

                if type(cells[count]) is int:
                        bname = b[count]
                        bname.config(command=partial(num_cell, count))

                if cells[count] == '@':
                        Mine(count, width, height)
        
                

        
       
def GamePage(x, y, number_of_mines):
        
    global root, b, cells, flag
        
    root = Toplevel()
    x1 = x*28
    y1 = y*28
    root.geometry("{}x{}".format(x1, y1))
    
    b = []
    w = [k for k in range(x*y)]

    # Generate random numbers for place of mines
    mineCells = random.sample(w, number_of_mines)

    # A list for determining mine cells, empty cells and number cells
    cells = [0]*(x*y)
    
    # A list for determining clicked cells
    # Each cell that been sweeped, determine by '1'.
    # Each one that isn't mine and is clicked determine by 1.
    flag = [0]*(x*y)

    # Mark the mine cells by '@'
    for t in mineCells:
        cells[t] = '@'
    
    # Build buttons of game
    count = 0       
    for i in range(x):
        for j in range(y):
            
            if count not in mineCells:        
                    neighbors = get_neighbors(count, x, y)

                    # Get number of mines that are around cell
                    q = 0
                    for char in neighbors:                    
                            if cells[char] == '@':
                                q += 1
                                
                    if q == 0:
                        cells[count] = '*'
                    else:
                            cells[count] = q
                
            btn = Button(root, width=2)
            btn.bind('<Button-1>', partial(left_click, count, x, y))
            btn.bind('<Button-3>', partial(right_click, count))
            btn.place(x=i*28, y=j*28)
            b.append(btn)
                                
            count += 1
            
             
    
def custom():
        
    window = Toplevel()
    window.title('Custom')
    window.geometry("250x250")
    
    label1 = Label(window, text="width")
    label1.place(x=0, y=0)
    label2 = Label(window, text="height")
    label2.place(x=0, y=30)
    label3 = Label(window, text="Percent mines")
    label3.place(x=0, y=60)


    def update_button1():
            button1.config(command=partial(GamePage, var2.get(), var1.get(),
                                           var3.get()))
            spin3.config(to=var1.get()*var2.get())

    # Build three spinbox for getting width & height & number of mines        
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    spin1 = Spinbox(window, from_=1, to=100, textvariable=var1, command=update_button1)
    spin1.place(x=100, y=0)
    spin2 = Spinbox(window, from_=1, to=100, textvariable=var2, command=update_button1)
    spin2.place(x=100, y=30)
    spin3 = Spinbox(window, from_=1, to=2, textvariable=var3, command=update_button1)
    spin3.place(x=100, y=60)
        
            

    button1 = Button(window, text="Play Game", width=32,
                     command=partial(GamePage, 1, 1, 1))
    button1.place(x=8, y=90)

    def close():
            window.destroy()
            
    button2 = Button(window, text="Cancel", width=32, command=close)  
    button2.place(x=8, y=125)
    
    
# First window
top = Tk()
top.title("Mine Sweeper")
top.geometry("400x400")
   
btn1 = Button(top, text="8x8 \n 10 mines", height=10, width=20, command=partial(GamePage, 8, 8, 10))
btn1.place(x=35, y=25)
btn2 = Button(top, text="16x16 \n 40 mines", height=10, width=20, command=partial(GamePage, 16, 16, 40))
btn2.place(x=200, y=25)
btn3 = Button(top, text="30x16 \n 99 mines", height=10, width=20, command=partial(GamePage, 30, 16, 99))
btn3.place(x=35, y=200)
btn4  = Button(top, text="? \n Custom", height=10, width=20, command=custom)
btn4.place(x=200, y=200)




top.mainloop()
