import os
from tkinter import *
import pandas as pd
from tkinter import ttk, filedialog
from tkinter import messagebox
import csv
import pymysql

class Student_Information:

    def __init__(self, root):
        self.root = root
        self.root.title('Student Information System')
        self.root.geometry('1200x555')
        self.root.resizable(False,False)

        self.ID_Number = StringVar()
        self.Full_Name = StringVar()
        self.Year_Level = StringVar()
        self.Gender = StringVar()
        self.Course_Code = StringVar()
        self.Course = StringVar()
        self.Search_by = StringVar()
        self.Search = StringVar()

        #==============Menu============
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Open", menu=self.file_menu)
        self.file_menu.add_command(label="Open a CSV file", command=self.file_open)

        self.save_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save as CSV file", command=self.save_info)

        #==============Frame============
        self.First_Frame = Frame(self.root, bd=8, relief=FLAT, bg='#fb8263')
        self.First_Frame.place(y=0, width=1366, height=53)

        self.Search_label = Label(self.First_Frame, text='Search by', font=('Lato', 14,'bold'),bg='#fb8263', fg='white', justify=RIGHT)
        self.Search_label.grid(padx=5, pady=0, ipady=2, row=0, column=0)

        self.Search_choice = ttk.Combobox(self.First_Frame, textvariable=self.Search_by, font=('Lato', 12), state='readonly',
                                                    values=['ID_Number', 'Full_Name'], width=10)
        self.Search_choice.current(0)
        self.Search_choice.grid(padx=5, pady=0, ipady=2, row=0, column=1)

        self.Search_entry = Entry(self.First_Frame, textvariable=self.Search, relief=FLAT, bg='white', font=('Lato', 12), width=15)
        self.Search_entry.grid(padx=5,ipady=3, row=0, column=2)

        self.Search_button = Button(self.First_Frame, text='Search',command=self.search, font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.Search_button.grid(padx=5,pady=0, ipady=2, row=0, column=3)

        self.Refresh_button = Button(self.First_Frame, text='Refresh', command=self.search_all, font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.Refresh_button.grid(padx=5, pady=0, ipady=2, row=0, column=4)

        self.Add_Student = Button(self.First_Frame, text='Add',command=self.add_student, font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.Add_Student.grid(padx=5, pady=0, ipady=2, row=0, column=5)

        self.Update_Student = Button(self.First_Frame, text='Update',command=self.update_student, font=('Century Gothic', 10), bg='#ffffff',relief=GROOVE)
        self.Update_Student.grid(padx=5, pady=0, ipady=2, row=0, column=6)

        self.Delete_Student = Button(self.First_Frame, text='Delete',command=self.delete, font=('Century Gothic', 10), bg='#ffffff',relief=GROOVE)
        self.Delete_Student.grid(padx=5, pady=0, ipady=2, row=0, column=7)

        self.Title = Label(self.First_Frame, text='STUDENT INFORMATION SYSTEM', font=('Century Gothic', 17,'bold'),bg='#fb8263', fg='white', justify=RIGHT)
        self.Title.grid(padx=155, pady=0, ipady=2, row=0, column=8)

        self.Details_Frame = Frame(self.root, bd=2, relief=FLAT, bg='white')
        self.Details_Frame.place(x=0, y=53, width=1200, height=500)

        # ============Scroll Bar and Treeview=========
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="#f1e2df",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#f1e2df"
                             )
        self.style.map("Treeview",
                       background=[('selected', '#f56f4c')])

        self.Student_Record = ttk.Treeview(self.Details_Frame, selectmode='browse')
        self.Student_Record["columns"] = ("ID Number", "Full Name", "Course Code", "Course", "Year Level", "Gender")

        self.scroll_horizontal = Scrollbar(self.Details_Frame, orient=HORIZONTAL)
        self.scroll_horizontal.pack(side=BOTTOM, fill=X)
        self.scroll_vertical = Scrollbar(self.Details_Frame, orient=VERTICAL)
        self.scroll_vertical.pack(side=RIGHT, fill=Y)

        self.Student_Record.config(yscrollcommand=self.scroll_vertical.set)
        self.Student_Record.config(xscrollcommand=self.scroll_horizontal.set)

        self.scroll_horizontal.config(command=self.Student_Record.xview)
        self.scroll_vertical.config(command=self.Student_Record.yview)

        self.Student_Record['show'] = 'headings'
        self.Student_Record.column("ID Number",anchor=CENTER, stretch=NO, width=100)
        self.Student_Record.column("Full Name", anchor=CENTER, stretch=NO, width=200)
        self.Student_Record.column("Course Code", anchor=CENTER, stretch=NO, width=100)
        self.Student_Record.column("Course",anchor=CENTER, stretch=YES, width=450)
        self.Student_Record.column("Year Level", anchor=CENTER, stretch=NO, width=100)
        self.Student_Record.column("Gender", anchor=CENTER, stretch=NO, width=200)

        self.Student_Record.heading("ID Number", text="ID Number")
        self.Student_Record.heading("Full Name", text="Full Name")
        self.Student_Record.heading("Course Code", text="Course Code")
        self.Student_Record.heading("Course", text="Course")
        self.Student_Record.heading("Year Level", text="Year Level")
        self.Student_Record.heading("Gender", text="Gender")

        self.Student_Record.pack(fill=BOTH, expand=1)
        self.Student_Record.bind("<ButtonRelease-1>", self.get_data)
        self.fetch_data()

     # Open A File Function
    def file_open(self):
        file_name = filedialog.askopenfilename(initialdir="C:/Users/", title="Open a File",
                                                   filetypes=(("csv files", "*.csv"), ("All Files", "*.*")))
        if file_name:
            try:
                filename = r"{}".format(file_name)
                data = pd.read_csv(filename)
            except ValueError:
                messagebox.showerror("Error", "File Could Not Be Opened")
            except FileNotFoundError:
                messagebox.showerror("Error", "File Could Not Be Found")

        self.clear_tree()

        self.Student_Record["column"] = list(data.columns)
        self.Student_Record["show"] = "headings"

        for column in self.Student_Record["column"]:
            self.Student_Record.column(column, anchor='center', stretch=NO)
            self.Student_Record.heading(column, text=column)

        data_rows = data.to_numpy().tolist()
        for row in data_rows:
            self.Student_Record.insert("", "end", values=row)

        self.Student_Record.pack()

    # Clear Current Tree
    def clear_tree(self):
        self.Student_Record.delete(*self.Student_Record.get_children())

    def save_info(self):
        if len(self.Student_Record.get_children()) < 1:
            messagebox.showinfo("No Data", "No data available to export")
            return False

        file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save CSV',
                                                filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
        with open(file, 'w', newline='') as output:
            output_data = csv.writer(output, delimiter=',')
            csv_writer = csv.writer(output, delimiter=',')
            csv_writer.writerow(['ID Number', 'Full Name', 'Course Code', 'Course', 'Year Level', 'Gender'])
            for x in self.Student_Record.get_children():
                row = self.Student_Record.item(x)['values']
                output_data.writerow(row)
        messagebox.showinfo("File Saved", "Data exported successfully!")

    def add_student(self):
        self.student_add()
        self.window = Toplevel(root)
        self.window.title("Adding...")
        self.window.resizable(False, False)
        self.window.geometry('800x250')

        self.Second_Frame = Frame(self.window, bd=2, relief=RIDGE, bg='#f1e2df')
        self.Second_Frame.place(width=799, height=399)

        self.Label_id = Label(self.Second_Frame, text='ID Number:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_id.grid(row=1, column=0, pady=10, padx=20, sticky='w')
        self.Label_id_entry = Entry(self.Second_Frame, textvariable=self.ID_Number, bg='#dcdad5', font=('Lato', 10), bd=2,relief=GROOVE)
        self.Label_id_entry.grid(row=1, column=1, ipady=3, pady=20, padx=0, sticky='w')

        self.Label_name = Label(self.Second_Frame, text='Full Name:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_name.grid(row=1, column=2, pady=10, padx=20, sticky='w')
        self.Label_name_entry = Entry(self.Second_Frame, textvariable=self.Full_Name, bg='#dcdad5', font=('Lato', 10), bd=2,relief=GROOVE)
        self.Label_name_entry.grid(row=1, column=3, ipady=3, pady=20, padx=20, sticky='w')

        self.Label_course_code = Label(self.Second_Frame, text='Course Code:', font=('Lato', 12), fg='#333438',bg='#f1e2df')
        self.Label_course_code.grid(row=2, column=0, pady=10, padx=20, sticky='w')
        self.Label_course_code_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Course_Code, font=('Lato', 10),
                                                    state='readonly', values=['SCS', 'CAS', 'COE', 'CSM', 'CED'], width=18)
        self.Label_course_code_entry.bind("<<ComboboxSelected>>", self.pick_color)
        self.Label_course_code_entry.grid(row=2, column=1, ipady=3, pady=20, padx=0, sticky='w')

        self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_course.grid(row=2, column=2, pady=10, padx=20, sticky='w')
        self.Label_course_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Course, font=('Lato', 10),state='readonly', values=[""],width=40)
        self.Label_course_entry.grid(row=2, column=3, ipady=3, pady=20, padx=20, sticky='w')

        self.Label_year = Label(self.Second_Frame, text='Year Level:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_year.grid(row=3, column=0, pady=10, padx=20, sticky='w')
        self.Label_year_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Year_Level, font=('Lato', 10),
                                             state='readonly',
                                             values=['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year',
                                                     'Other'], width=18)
        self.Label_year_entry.grid(row=3, column=1, ipady=3, pady=20, padx=0, sticky='w')

        self.Label_gender = Label(self.Second_Frame, text='Gender:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_gender.grid(row=3, column=2, pady=10, padx=20, sticky='w')
        self.Label_gender_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Gender, font=('Lato', 10),
                                               state='readonly', values=['Male', 'Female'], width=18)
        self.Label_gender_entry.grid(row=3, column=3, ipady=3, pady=20, padx=20, sticky='w')

        self.Add = Button(self.Second_Frame, text='Add', font=('Century Gothic', 12), command=self.add,
                             bg='#fb8263', relief=GROOVE)
        self.Add.place(x=650, y=200)

        self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 12), command=self.clear,
                            bg='#fb8263', relief=GROOVE)
        self.Clear.place(x=720, y=200)

    def student_add(self):
        self.ID_Number.set('')
        self.Full_Name.set('')
        self.Year_Level.set('')
        self.Gender.set('')
        self.Course.set('')
        self.Course_Code.set('')

    def add(self):
        if (len(self.ID_Number.get()) == 0 or len(self.Full_Name.get()) == 0 or len(
                self.Year_Level.get()) == 0 or len(self.Gender.get()) == '' or len(self.Course.get()) == 0):
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="student_information_system")
            cursor = connect.cursor()
            cursor.execute("insert into students values (%s, %s, %s, %s, %s, %s)", (self.ID_Number.get(),
                                                                                    self.Full_Name.get(),
                                                                                    self.Course_Code.get(),
                                                                                    self.Course.get(),
                                                                                    self.Year_Level.get(),
                                                                                    self.Gender.get()))
            connect.commit()
            self.fetch_data()
            connect.close()
            messagebox.showinfo("Success", "You added a new student!")

            self.clear()
            self.window.destroy()

    def fetch_data(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="student_information_system")
        cursor = connect.cursor()
        cursor.execute("select * from students")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record.delete(*self.Student_Record.get_children())
            for row in rows:
                self.Student_Record.insert('', END, values=row)
            connect.commit()
        connect.close()

    def update_student(self):
        answer = messagebox.askyesno("Update Student Data", "Do you want to update data?")
        if not answer:
            pass
        else:
            self.window = Toplevel(root)
            self.window.title("Updating...")
            self.window.resizable(False, False)
            self.window.geometry('800x250')

            self.Second_Frame = Frame(self.window, bd=2, relief=RIDGE, bg='#f1e2df')
            self.Second_Frame.place(width=799, height=399)

            self.Label_id = Label(self.Second_Frame, text='ID Number:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_id.grid(row=1, column=0, pady=10, padx=20, sticky='w')
            self.Label_id_entry = Entry(self.Second_Frame, textvariable=self.ID_Number, bg='#dcdad5', font=('Lato', 10),
                                        bd=2, relief=GROOVE)
            self.Label_id_entry.grid(row=1, column=1, ipady=3, pady=20, padx=0, sticky='w')

            self.Label_name = Label(self.Second_Frame, text='Full Name:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_name.grid(row=1, column=2, pady=10, padx=20, sticky='w')
            self.Label_name_entry = Entry(self.Second_Frame, textvariable=self.Full_Name, bg='#dcdad5',
                                          font=('Lato', 10), bd=2, relief=GROOVE)
            self.Label_name_entry.grid(row=1, column=3, ipady=3, pady=20, padx=20, sticky='w')

            self.Label_course_code = Label(self.Second_Frame, text='Course Code:', font=('Lato', 12), fg='#333438',
                                           bg='#f1e2df')
            self.Label_course_code.grid(row=2, column=0, pady=10, padx=20, sticky='w')
            self.Label_course_code_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Course_Code,
                                                        font=('Lato', 10),
                                                        state='readonly', values=['SCS', 'CAS', 'COE', 'CSM', 'CED'],
                                                        width=18)
            self.Label_course_code_entry.bind("<<ComboboxSelected>>", self.pick_color)
            self.Label_course_code_entry.grid(row=2, column=1, ipady=3, pady=20, padx=0, sticky='w')

            self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_course.grid(row=2, column=2, pady=10, padx=20, sticky='w')
            self.Label_course_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Course, font=('Lato', 10),
                                                   state='readonly', values=[""], width=40)
            self.Label_course_entry.grid(row=2, column=3, ipady=3, pady=20, padx=20, sticky='w')

            self.Label_year = Label(self.Second_Frame, text='Year Level:', font=('Lato', 12), fg='#333438',
                                    bg='#f1e2df')
            self.Label_year.grid(row=3, column=0, pady=10, padx=20, sticky='w')
            self.Label_year_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Year_Level, font=('Lato', 10),
                                                 state='readonly',
                                                 values=['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year',
                                                         'Other'], width=18)
            self.Label_year_entry.grid(row=3, column=1, ipady=3, pady=20, padx=0, sticky='w')

            self.Label_gender = Label(self.Second_Frame, text='Gender:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_gender.grid(row=3, column=2, pady=10, padx=20, sticky='w')
            self.Label_gender_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Gender, font=('Lato', 10),
                                                   state='readonly', values=['Male', 'Female'], width=18)
            self.Label_gender_entry.grid(row=3, column=3, ipady=3, pady=20, padx=20, sticky='w')

            self.Update = Button(self.Second_Frame, text='Update', font=('Century Gothic', 12), command=self.update,
                              bg='#fb8263', relief=GROOVE)
            self.Update.place(x=620, y=200)

            self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 12), command=self.clear,
                                bg='#fb8263', relief=GROOVE)
            self.Clear.place(x=720, y=200)

    def update(self):
        if (len(self.ID_Number.get()) == 0 or len(self.Full_Name.get()) == 0 or len(
                self.Year_Level.get()) == 0 or len(self.Gender.get()) == '' or len(self.Course.get()) == 0):
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="student_information_system")
            cursor = connect.cursor()
            cursor.execute("update students set Full_Name=%s, Course_code=%s, Course=%s, Year_Level=%s, Gender=%s where ID_Number=%s",(
                                                                                    self.Full_Name.get(),
                                                                                    self.Course_Code.get(),
                                                                                    self.Course.get(),
                                                                                    self.Year_Level.get(),
                                                                                    self.Gender.get(),
                                                                                    self.ID_Number.get()))
            connect.commit()
            self.fetch_data()
            self.clear()
            connect.close()
            messagebox.showinfo("Success", "You updated the record!")

            self.window.destroy()
            self.Search_entry.delete(0, END)

    def pick_color(self, e):
        self.SCS = ['Bachelor Of Science In Information Systems',
                    'Bachelor Of Science In Information Technology', 'Diploma In Electronics Technology',
                    'Diploma In Electronics Technology',
                    'Diploma In Electronics Engineering Tech',
                    'Bachelor Of Science In Computer Science',
                    'Bachelor Of Science In Electronics And Computer Technology']

        self.CAS = ['General Education Program', 'Bachelor Of Arts In English', 'Bachelor Of Science In Psychology',
                    'Bachelor Of Arts In Filipino', 'Bachelor Of Arts In History',
                    'Bachelor Of Arts In Political Science']

        self.COE = ['Diploma In Chemical Engineering Technology', 'Bachelor Of Science In Civil Engineering',
                    'Bachelor Of Science In Ceramics Engineering', 'Bachelor Of Science In Chemical Engineering',
                    'Bachelor Of Science In Computer Engineering',
                    'Bachelor Of Science In Electronics & Communications Engineering',
                    'Bachelor Of Science In Electrical Engineering', 'Bachelor Of Science In Mining Engineering',
                    'Bachelor Of Science In Environmental Engineering Technology',
                    'Bachelor Of Science In Mechanical Engineering',
                    'Bachelor Of Science Metallurgical Engineering']

        self.CSM = ['Bachelor Of Science In Biology (Botany)', 'Bachelor Of Science In Chemistry',
                    'Bachelor Of Science In Mathematics',
                    'Bachelor Of Science In Physics', 'Bachelor Of Science In Biology (Zoology)',
                    'Bachelor Of Science In Biology (Marine)',
                    'Bachelor Of Science In Biology (General)', 'Bachelor Of Science In Statistics']

        self.CED = ['Bachelor Of Secondary Education (Biology)',
                    'Bachelor Of Science In Industrial Education (Drafting)',
                    'Bachelor Of Secondary Education (Chemistry)', 'Bachelor Of Secondary Education (Physics)',
                    'Bachelor Of Secondary Education (Mathematics)', 'Bachelor Of Secondary Education (Mapeh)',
                    'Certificate Program For Teachers', 'Bachelor Of Secondary Education (Tle)',
                    'Bachelor Of Secondary Education (General Science)',
                    'Bachelor Of Elementary Education (English)',
                    'Bachelor Of Elementary Education (Science And Health)',
                    'Bachelor Of Science In Technology Teacher Education (Industrial Tech)',
                    'Bachelor Of Science In Technology Teacher Education (Drafting Tech)']

        if self.Label_course_code_entry.get() == 'SCS':
            self.Label_course_entry.config(values=self.SCS)

        if self.Label_course_code_entry.get() == 'CAS':
            self.Label_course_entry.config(values=self.CAS)

        if self.Label_course_code_entry.get() == 'COE':
            self.Label_course_entry.config(values=self.COE)

        if self.Label_course_code_entry.get() == 'CSM':
            self.Label_course_entry.config(values=self.CSM)

        if self.Label_course_code_entry.get() == 'CED':
            self.Label_course_entry.config(values=self.CED)

    def delete(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="student_information_system")
        cursor = connect.cursor()
        cursor.execute("delete from students where id_number=%s", self.ID_Number.get())
        connect.commit()
        connect.close()
        self.fetch_data()
        self.clear()

        messagebox.showinfo("Deleted", "Record has been deleted")

    def clear(self):
        self.ID_Number.set("")
        self.Full_Name.set("")
        self.Course_Code.set('')
        self.Course.set('')
        self.Year_Level.set('')
        self.Gender.set('')

    def search(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="student_information_system")
        cursor = connect.cursor()
        cursor.execute("select * from students where " + str(self.Search_by.get()) +" Like '%"+str(self.Search.get())+"%' ")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record.delete(*self.Student_Record.get_children())
            for row in rows:
                self.Student_Record.insert('', END, values=row)
            connect.commit()
        connect.close()

    def search_all(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="student_information_system")
        cursor = connect.cursor()
        cursor.execute("select * from students")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record.delete(*self.Student_Record.get_children())
            for row in rows:
                self.Student_Record.insert('', END, values=row)
            connect.commit()
        connect.close()

        self.Search_entry.delete(0, END)

    def get_data(self, e):
        selected = self.Student_Record.focus()
        values = self.Student_Record.item(selected, 'values')

        self.ID_Number.set(values[0])
        self.Full_Name.set(values[1])
        self.Course_Code.set(values[2])
        self.Course.set(values[3])
        self.Year_Level.set(values[4])
        self.Gender.set(values[5])

root = Tk()
ob = Student_Information(root)
root.mainloop()