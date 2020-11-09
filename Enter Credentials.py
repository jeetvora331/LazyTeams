from tkinter import *
import json
 
window = Tk()
window.geometry('250x100')
window.title('LazyTeams')
 


def check():
    a = Username.get()
    b = (Pwd.get())
    c = Minp.get()
    print(a)
    print(b)
    print(c)
    data = {}
    data['username'] = a
    data['password'] = b
    data['min_parti'] = c
    files = [('JSON File', '*.json')]
    fileName='cred'
    writeToJSONFile(fileName, data)
    window.destroy()
     

username = Label(window, text="User ID:")
Username = Entry(window)
pwd = Label(window, text="Password:")
Pwd = Entry(window,show='*')
minp = Label(window, text="Min Participants:")
Minp = Entry(window)
submit = Button(window,text='Submit',command = check).grid(row=3, column=1)

test = 1
def writeToJSONFile(fileName, data):
    filePathNameWExt = fileName+'.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path = './'

 
username.grid(row=0, column=0)
pwd.grid(row=1,column=0)
minp.grid(row=2,column=0)
Username.grid(row=0, column=1)
Pwd.grid(row=1, column=1)
Minp.grid(row=2, column=1)
 
 
mainloop()