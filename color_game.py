import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import mysql.connector as mysql
import random
from widgets import PlaceholderEntry, ToolTip

root = tk.Tk()
root.title('Color finder game')
root.resizable(0,0)
root.iconbitmap('img/color.ico')

timer = 30
score = 0

def dbase():
    con = mysql.connect(host='',username='',password='',database='')
    c = con.cursor()
    c.execute('SELECT `Name` from scores;')
    recs = c.fetchall()
    names = []

    for rec in recs:
        names.append(rec[0])
    
    if name.acquire() in names:
        c.execute(f'UPDATE scores SET Score = Score+{score} where `Name` = %s;',(name.acquire(),))
        con.commit()
    
    else:
        c.execute('INSERT INTO scores(`Name`,`Score`) VALUES(%s,%s)',(name.acquire(),score))
        con.commit()
    
    con.close()

def update():
    global score
    
    if name.acquire() == 'None':
        messagebox.showerror('Name required','Please enter your name to continue')
    
    else:
        e.focus()
        b['state'] = 'disabled'
        b1['state'] = 'disabled'
        b2['state'] = 'disabled'
        name['state'] = 'disabled'

        def time():
            global timer, a
            if timer > 0:
                timer -= 1
                timer_label.config(text=f'Time left: {timer}')
                a = root.after(1000,time)
            
            else:
                root.after_cancel(a)
                e.unbind('<Return>')
                b['state'] = 'normal'
                b1['state'] = 'normal'
                b2['state'] = 'normal'
                messagebox.showinfo('Score',f'Your score is {score}')
                dbase()

        def check(event):
            global num_t, num_c, score

            if e.acquire().lower() == colors[num_c].lower():
                score += 1
                score_label.config(text=f'Score: {score}')

            num_t = random.randint(0,len(colors)-1)
            num_c = random.randint(0,len(colors)-1)
            color_label.config(text=text[num_t],fg=colors[num_c])
            e.remove(0,'end')

        if timer > 0:
            color_label.config(text=text[num_t],fg=colors[num_c])
            e.bind('<Return>',check)
            time()
        
def restart():
    global score, timer
    score = 0
    timer = 30
    score_label.config(text=f'Score: {score}')
    update()

def board():
    log = tk.Toplevel(root)
    log.title('Leaderboard')
    log.focus_force()
    log.geometry('+150+200')
    log.geometry('800x800')
    log.iconbitmap('img/search.ico')

    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, text=col, command=lambda _col=col: treeview_sort_column(
            tv, _col, not reverse))

    # Number of data fetched
    cone = mysql.connect(host='',username='',password='',database='')
    ca = cone.cursor()
    sql_command_01 = 'SELECT * FROM scores;'
    ca.execute(sql_command_01)
    result = ca.fetchall()

    tk.Label(log,text='Leaderboard',font=(0,19)).grid(row=0,column=0)
    # setup treeview
    columns = (('Sl.no.',50),('Name', 120), ('Score', 80))
    tree = ttk.Treeview(log, height=20, columns=[x[0] for x in columns], show='headings')
    tree.grid(row=1, column=0, sticky='news')
    
    log.rowconfigure(1,weight=1)
    log.columnconfigure(0,weight=1)
    
    # setup columns attributes
    for col, width in columns:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, width=width, anchor=tk.CENTER)

    # fetch data
    con = mysql.connect(host='',username='',password='',database='')
    c = con.cursor()
    sql_command_1 = 'SELECT * FROM scores order by Score DESC;'
    c.execute(sql_command_1)

    # populate data to treeview
    for rec in c:
        tree.insert('', 'end', value=rec)

    def pop_menu(event):
        global column
        tree.identify_row(event.y)
        column = tree.identify_column(event.x)
        popup1.post(event.x_root, event.y_root)

    def copy():
        row_id = tree.selection()
        column_no = column
        select = tree.set(row_id, column_no)
        log.clipboard_append(select)
        log.update()

    popup1 = tk.Menu(log, tearoff=0)
    popup1.add_command(label='Copy', command=copy)

    tree.bind('<Button-3>', pop_menu)

    # scrollbar
    sb = tk.Scrollbar(log, orient=tk.VERTICAL, command=tree.yview)
    sb.grid(row=1, column=1, sticky='ns')
    tree.config(yscrollcommand=sb.set)
    a = tree.item(tree.focus())['values']

    btn = tk.Button(log, text='Close', command=log.destroy,
                    width=20, bd=2, fg='red')
    btn.grid(row=3, column=0, columnspan=2, sticky=tk.E+tk.W)
    status = tk.Label(
        log, text=f'Total records fetched: {len(result)}', bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status.grid(row=2, columnspan=2, sticky=tk.E+tk.W)
    con.close()
    cone.close()

colors = ['Yellow','Blue','Red','Green','Black','Brown','Purple','Orange','Violet']
text = ['Blue','Black','Yellow','Green','Red','Purple','Brown','Violet','Orange']

num_t = random.randint(0,len(colors)-1)
num_c = random.randint(0,len(colors)-1)

color_label = tk.Label(root,text=text[num_t],fg=colors[num_c],font=(0,30,'bold'))
color_label.grid(row=2,column=0,padx=10,pady=10)

timer_label = tk.Label(root,text=f'Time left: {timer}',font=(0,12))
timer_label.grid(row=0,column=0,pady=5)

score_label = tk.Label(root,text=f'Score: {score}',font=(0,12))
score_label.grid(row=1,column=0)

name = PlaceholderEntry(root,placeholder='Eg: Nihaal',width=30,font=(0,13))
name.grid(row=3,column=0,pady=10,padx=10,ipady=5)

e = PlaceholderEntry(root,placeholder='Enter the color of the text',width=30,font=(0,13))
e.grid(row=4,column=0,pady=10,padx=10,ipady=5)

b = ttk.Button(root,text='Start',command=update)
b.grid(row=5,column=0,pady=10)

b1 = ttk.Button(root,text='Restart',command=restart)
b1.grid(row=6,column=0,pady=(0,5))

b2 = ttk.Button(root,text='Leaderboard',command=board)
b2.grid(row=7,column=0,pady=(0,5))

ins_label = tk.Label(root,text='Hover here for instruction',font=(0,15))
ins_label.grid(row=8,column=0,pady=5)

ins_tooltip = ToolTip(ins_label,'Press the Start button and type the COLOR of text in the blank and press enter key to proceed.\nPress Restart button to try again.\nYou have 30 seconds over each try, all the best\n\n Made by: Nihaal Nz')

# Trying to establish database connection
try:
    mysql.connect(host='',username='',password='',database='')
                    
except:
    messagebox.showerror('Connection Failed','Connection with the database could not be established.\nPlease try again later.',parent=root)
    root.destroy()


root.mainloop()