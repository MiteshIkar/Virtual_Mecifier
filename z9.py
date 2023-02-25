import http.client

conn = http.client.HTTPSConnection("v1.genr.ai")
FNAME = ""

class SomeClass:
    def func_1(self, FNAME):
        file1 = open(FNAME)
        
        s = ""
        
        for line in file1:
            s = s + line 
        
        file1.close()

        payload = "{\n  \"text\": \"" + s + "\",\n  \"temperature\": 0,\n  \"max_words\": 15\n}"

        headers = { 'Content-Type': "application/json" }

        conn.request("POST", "/api/circuit-element/summarize", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))

        win = Tk()
        win.geometry("450x300")
        
        s = data.decode("utf-8")
        
        l1 = Label(win,
                  text = "Summary of text: " + s[11:-2]).place(x = 40, y = 60)
        
        win.mainloop()

from tkinter import *

from tkinter import filedialog

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/Desktop",
                      title = "Select a File",
                      filetypes = (("Text files",
                              "*.txt*"),
                            ("all files",
                              "*.*")))
    
    label_file_explorer.configure(text="File Opened: " + filename)
    FNAME = filename
    s = SomeClass()
    s.func_1(FNAME)


window = Tk()

window.title('File Explorer')

window.geometry("700x500")

window.config(background = "white")

label_file_explorer = Label(window,
							text = "File Explorer using Tkinter",
							width = 100, height = 4,
							fg = "blue")

	
button_explore = Button(window,
						text = "Browse Files",
						command = browseFiles,
                        height = 10,
                        width = 30)

button_exit = Button(window,
					text = "Exit",
					command = exit,
                        height = 10,
                        width = 30)

label_file_explorer.grid(column = 1, row = 1, pady = 5)

button_explore.grid(column = 1, row = 2, pady = 5)

button_exit.grid(column = 1,row = 3)

window.mainloop()

