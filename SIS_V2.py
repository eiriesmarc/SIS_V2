from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


class SIS:

    def __init__(self, root):
        self.root = root
        self.root.title('Student Information System')
        self.root.geometry('770x600')
        self.root.resizable(False, False)

        self.var = ''
        self.var_course = ''

        self.ID_Number = StringVar()
        self.Full_Name = StringVar()
        self.Course = StringVar()
        self.Year_Level = StringVar()
        self.Gender = StringVar()
        self.Search_by = StringVar()
        self.Search = StringVar()

        self.Search_course = StringVar()
        self.Course_code = StringVar()
        self.Course_name = StringVar()

        # ==============Frame============
        self.first_frame = Frame(self.root, bd=8, relief=FLAT, bg='#fb8263')
        self.first_frame.place(y=0, width=1366, height=53)

        self.search_label = Label(self.first_frame, text='Search by', font=('Lato', 14, 'bold'), bg='#fb8263',
                                  fg='white', justify=RIGHT)
        self.search_label.grid(padx=5, pady=0, ipady=2, row=0, column=0)

        self.search_choice = ttk.Combobox(self.first_frame, textvariable=self.Search_by, font=('Lato', 12),state='readonly',
                                          values=['ID_Number', 'Full_Name', 'Course'], width=10)
        self.search_choice.current(0)
        self.search_choice.grid(padx=5, pady=0, ipady=2, row=0, column=1)

        self.search_entry = Entry(self.first_frame, textvariable=self.Search, relief=FLAT, bg='white',
                                  font=('Lato', 12), width=15)
        self.search_entry.grid(padx=5, ipady=3, row=0, column=2)

        self.search_button = Button(self.first_frame, text='Search', command=self.search, font=('Century Gothic', 10),
                                    bg='#ffffff', relief=GROOVE)
        self.search_button.grid(padx=5, pady=0, ipady=2, row=0, column=3)

        self.refresh_button = Button(self.first_frame, text='Refresh', command=self.refresh,
                                     font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.refresh_button.grid(padx=5, pady=0, ipady=2, row=0, column=4)

        self.add_student = Button(self.first_frame, text='Add', command=self.adding_student, font=('Century Gothic', 10),
                                  bg='#ffffff', relief=GROOVE)
        self.add_student.grid(padx=5, pady=0, ipady=2, row=0, column=5)

        self.update_student = Button(self.first_frame, text='Edit', command=self.updating_student,
                                     font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.update_student.grid(padx=5, pady=0, ipady=2, row=0, column=6)

        self.delete_student = Button(self.first_frame, text='Delete', command=self.delete, font=('Century Gothic', 10),
                                     bg='#ffffff', relief=GROOVE)
        self.delete_student.grid(padx=5, pady=0, ipady=2, row=0, column=7)

        self.details_frame = Frame(self.root, bd=2, relief=FLAT, bg='white')
        self.details_frame.place(x=0, y=53, width=770, height=500)

        self.below_frame = Frame(self.root, bd=5, relief=RIDGE, bg='#fb8263')
        self.below_frame.place(y=550, width=769, height=51)

        self.manage_courses = Button(self.below_frame, text='Manage Courses', command=self.open_courses,font=('Century Gothic', 10), bg='#ffffff',
                                  relief=GROOVE)
        self.manage_courses.grid(padx=5, pady=2, ipady=2, row=0, column=1, sticky=W)

        self.title = Label(self.below_frame, text='STUDENT INFORMATION SYSTEM', font=('Century Gothic', 17, 'bold'),
                           bg='#fb8263', fg='white')
        self.title.grid(padx=280, pady=2, ipady=2, row=0, column=2, sticky=W)

        # ============Scroll Bar and Treeview=========
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.style.configure("Treeview",
                             background="#f1e2df",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#f1e2df"
                             )
        self.style.map("Treeview",
                       background=[('selected', '#f56f4c')])

        self.Student_Record = ttk.Treeview(self.details_frame, selectmode='browse')
        self.Student_Record["columns"] = ("ID Number", "Full Name", "Course", "Year Level", "Gender")

        self.scroll_horizontal = Scrollbar(self.details_frame, orient=HORIZONTAL)
        self.scroll_horizontal.pack(side=BOTTOM, fill=X)
        self.scroll_vertical = Scrollbar(self.details_frame, orient=VERTICAL)
        self.scroll_vertical.pack(side=RIGHT, fill=Y)

        self.Student_Record.config(yscrollcommand=self.scroll_vertical.set)
        self.Student_Record.config(xscrollcommand=self.scroll_horizontal.set)

        self.scroll_horizontal.config(command=self.Student_Record.xview)
        self.scroll_vertical.config(command=self.Student_Record.yview)

        self.Student_Record['show'] = 'headings'
        self.Student_Record.column("ID Number", anchor=CENTER, stretch=NO, width=140)
        self.Student_Record.column("Full Name", anchor=CENTER, stretch=NO, width=200)
        self.Student_Record.column("Course", anchor=CENTER, stretch=NO, width=140)
        self.Student_Record.column("Year Level", anchor=CENTER, stretch=NO, width=140)
        self.Student_Record.column("Gender", anchor=CENTER, stretch=NO, width=125)

        self.Student_Record.heading("ID Number", text="ID Number")
        self.Student_Record.heading("Full Name", text="Full Name")
        self.Student_Record.heading("Course", text="Course")
        self.Student_Record.heading("Year Level", text="Year Level")
        self.Student_Record.heading("Gender", text="Gender")

        self.Student_Record.pack(fill=BOTH, expand=True)
        self.Student_Record.bind("<ButtonRelease-1>", self.get_data)
        self.fetch_data()

    def load_combobox(self):
        connect = pymysql.connect(host='localhost', user="root", password="", database="sis_v2")
        cursor = connect.cursor()
        mysql = 'SELECT course_code from courses'
        cursor.execute(mysql)

        data = []

        for row in cursor.fetchall():
            data.append(row[0])

        return data

        #======Functions======
    def adding_student(self):
        self.student_add()
        self.window = Toplevel(root)
        self.window.title("Adding...")
        self.window.resizable(False, False)
        self.window.geometry('760x200')

        self.Second_Frame = Frame(self.window, bd=2, relief=RIDGE, bg='#f1e2df')
        self.Second_Frame.place(width=799, height=399)

        self.Label_id = Label(self.Second_Frame, text='ID Number:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_id.grid(row=1, column=0, pady=10, padx=20, sticky='w')
        self.Label_id_entry = Entry(self.Second_Frame, textvariable=self.ID_Number, bg='#dcdad5', font=('Lato', 10), bd=2,relief=GROOVE)
        self.Label_id_entry.grid(row=1, column=1, ipady=3, pady=20, padx=0, sticky='w')

        self.Label_name = Label(self.Second_Frame, text='Full Name:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_name.grid(row=2, column=0, pady=0, padx=20, sticky='w')
        self.Label_name_entry = Entry(self.Second_Frame, textvariable=self.Full_Name, bg='#dcdad5', font=('Lato', 10), bd=2,relief=GROOVE)
        self.Label_name_entry.grid(row=2, column=1, ipady=3, pady=0, padx=0, sticky='w')

        self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_course.grid(row=1, column=2, pady=10, padx=20, sticky='w')
        self.Label_course_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Course, state='readonly', font=('Lato', 10), width=40)
        self.Label_course_entry['values'] = self.load_combobox()
        self.Label_course_entry.grid(row=1, column=3, ipady=3, pady=0, padx=0, sticky='w')

        self.Label_year = Label(self.Second_Frame, text='Year Level:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_year.grid(row=3, column=0, pady=10, padx=20, sticky='w')
        self.Label_year_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Year_Level, font=('Lato', 10), state='readonly',
                                        values=['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year', 'Other'], width=18)
        self.Label_year_entry.grid(row=3, column=1, ipady=3, pady=0, padx=0, sticky='w')

        self.Label_gender = Label(self.Second_Frame, text='Gender:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_gender.grid(row=2, column=2, pady=10, padx=20, sticky='w')
        self.Label_gender_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Gender, font=('Lato', 10),
                                               state='readonly', values=['Male', 'Female'], width=18)
        self.Label_gender_entry.grid(row=2, column=3, ipady=3, pady=20, padx=0, sticky='w')

        self.Add = Button(self.Second_Frame, text='Add', font=('Century Gothic', 12), command=self.add,
                             bg='#fb8263', relief=GROOVE)
        self.Add.place(x=610, y=85)

        self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 12), command=self.clear,
                            bg='#fb8263', relief=GROOVE)
        self.Clear.place(x=680, y=85)

        self.Adding = Label(self.Second_Frame, text="INPUT STUDENT'S DATA...", font=('Century Gothic', 18, 'bold'), fg='#333438', bg='#f1e2df')
        self.Adding.place(x=460, y=140)

    def student_add(self):
        self.ID_Number.set('')
        self.Full_Name.set('')
        self.Year_Level.set('')
        self.Gender.set('')
        self.Course.set('')

    def add(self):
        if (len(self.ID_Number.get()) == 0 or len(self.Full_Name.get()) == 0 or
                len(self.Year_Level.get()) == 0 or len(self.Gender.get()) == 0 or len(self.Course.get()) == 0):
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
            cursor = connect.cursor()
            cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s, %s)",
                                                        (self.ID_Number.get(),
                                                        self.Full_Name.get(),
                                                        self.Course.get(),
                                                        self.Year_Level.get(),
                                                        self.Gender.get()))
            connect.commit()
            self.fetch_data()
            connect.close()
            messagebox.showinfo("Success", "You added a new student!")

            self.clear()
            self.window.destroy()

    def updating_student(self):
        answer = messagebox.askyesno("Update Student Data", "Do you want to update data?")
        if not answer:
            pass
        else:
            self.window = Toplevel(root)
            self.window.title("Updating...")
            self.window.resizable(False, False)
            self.window.geometry('760x200')

            self.Second_Frame = Frame(self.window, bd=2, relief=RIDGE, bg='#f1e2df')
            self.Second_Frame.place(width=799, height=399)

            self.Label_id = Label(self.Second_Frame, text='ID Number:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_id.grid(row=1, column=0, pady=10, padx=20, sticky='w')
            self.Label_id_entry = Entry(self.Second_Frame, textvariable=self.ID_Number, bg='#dcdad5', font=('Lato', 10),
                                        bd=2, relief=GROOVE)
            self.Label_id_entry.grid(row=1, column=1, ipady=3, pady=20, padx=0, sticky='w')

            self.Label_name = Label(self.Second_Frame, text='Full Name:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_name.grid(row=2, column=0, pady=0, padx=20, sticky='w')
            self.Label_name_entry = Entry(self.Second_Frame, textvariable=self.Full_Name, bg='#dcdad5',
                                          font=('Lato', 10), bd=2, relief=GROOVE)
            self.Label_name_entry.grid(row=2, column=1, ipady=3, pady=0, padx=0, sticky='w')

            self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_course.grid(row=1, column=2, pady=10, padx=20, sticky='w')
            self.Label_course_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Course, state='readonly',
                                                   font=('Lato', 10), width=40)
            self.Label_course_entry['values'] = self.load_combobox()
            self.Label_course_entry.grid(row=1, column=3, ipady=3, pady=0, padx=0, sticky='w')

            self.Label_year = Label(self.Second_Frame, text='Year Level:', font=('Lato', 12), fg='#333438',
                                    bg='#f1e2df')
            self.Label_year.grid(row=3, column=0, pady=10, padx=20, sticky='w')
            self.Label_year_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Year_Level, font=('Lato', 10),
                                                 state='readonly',
                                                 values=['1st Year', '2nd Year', '3rd Year', '4th Year', '5th Year',
                                                         'Other'], width=18)
            self.Label_year_entry.grid(row=3, column=1, ipady=3, pady=0, padx=0, sticky='w')

            self.Label_gender = Label(self.Second_Frame, text='Gender:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_gender.grid(row=2, column=2, pady=10, padx=20, sticky='w')
            self.Label_gender_entry = ttk.Combobox(self.Second_Frame, textvariable=self.Gender, font=('Lato', 10),
                                                   state='readonly', values=['Male', 'Female'], width=18)
            self.Label_gender_entry.grid(row=2, column=3, ipady=3, pady=20, padx=0, sticky='w')

            self.Update = Button(self.Second_Frame, text='Update', font=('Century Gothic', 12), command=self.update,
                              bg='#fb8263', relief=GROOVE)
            self.Update.place(x=590, y=85)

            self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 12), command=self.clear,
                                bg='#fb8263', relief=GROOVE)
            self.Clear.place(x=680, y=85)

            self.Updating = Label(self.Second_Frame, text="UPDATE STUDENT'S DATA...",
                                font=('Century Gothic', 18, 'bold'), fg='#333438', bg='#f1e2df')
            self.Updating.place(x=440, y=140)

    def update(self):
        if (len(self.ID_Number.get()) == 0 or len(self.Full_Name.get()) == 0 or len(
                self.Year_Level.get()) == 0 or len(self.Gender.get()) == '' or len(self.Course.get()) == 0):
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
            cursor = connect.cursor()
            var = self.ID_Number.get()
            cursor.execute(f"UPDATE students SET Full_Name='{self.Full_Name.get()}', Course='{self.Course.get()}', ID_Number='{self.ID_Number.get()}', "
                           f"Year_Level='{self.Year_Level.get()}', Gender='{self.Gender.get()}' WHERE ID_Number='{self.var}'")
            connect.commit()
            self.fetch_data()
            self.clear()
            connect.close()
            messagebox.showinfo("Success", "You updated the record!")

            self.window.destroy()

            self.search_entry.delete(0, END)

    def open_courses(self):
        self.second_window = Toplevel()
        self.second_window.title('Manage Courses')
        self.second_window.geometry('730x300')
        self.second_window.resizable(False, False)

        # ==============Frame============
        self.first_frame1 = Frame(self.second_window, bd=8, relief=FLAT, bg='#fb8263')
        self.first_frame1.place(y=0, width=1366, height=53)

        self.search_entry1 = Entry(self.second_window, textvariable=self.Search_course, relief=FLAT, bg='white',
                                  font=('Lato', 12), width=15)
        self.search_entry1.grid(padx=5, pady=11, ipady=3, row=0, column=2)

        self.search_button1 = Button(self.second_window, text='Search Code', command=self.search_courses, font=('Century Gothic', 10),
                                    bg='#ffffff', relief=GROOVE)
        self.search_button1.grid(padx=5, pady=0, ipady=2, row=0, column=3)

        self.refresh_button1 = Button(self.second_window, text='Refresh', command=self.fetch_courses,
                                     font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.refresh_button1.grid(padx=5, pady=0, ipady=2, row=0, column=4)

        self.add_student1 = Button(self.second_window, text='Add',command=self.adding_courses, font=('Century Gothic', 10),
                                  bg='#ffffff', relief=GROOVE)
        self.add_student1.grid(padx=5, pady=0, ipady=2, row=0, column=5)

        self.update_student1 = Button(self.second_window, text='Edit', command=self.updating_courses,
                                     font=('Century Gothic', 10), bg='#ffffff', relief=GROOVE)
        self.update_student1.grid(padx=5, pady=0, ipady=2, row=0, column=6)

        self.delete_student1 = Button(self.second_window, text='Delete', command=self.delete_courses, font=('Century Gothic', 10),
                                     bg='#ffffff', relief=GROOVE)
        self.delete_student1.grid(padx=5, pady=0, ipady=2, row=0, column=7)

        self.details_frame1 = Frame(self.second_window, bd=2, relief=FLAT, bg='white')
        self.details_frame1.place(x=0, y=53, width=730, height=248)

        # ============Scroll Bar and Treeview=========
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.style.configure("Treeview",
                             background="#f1e2df",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#f1e2df"
                             )
        self.style.map("Treeview",
                       background=[('selected', '#f56f4c')])

        self.Student_Record1 = ttk.Treeview(self.details_frame1, selectmode='browse')
        self.Student_Record1["columns"] = ("Course Code", "Course")

        self.scroll_horizontal = Scrollbar(self.details_frame1, orient=HORIZONTAL)
        self.scroll_horizontal.pack(side=BOTTOM, fill=X)
        self.scroll_vertical = Scrollbar(self.details_frame1, orient=VERTICAL)
        self.scroll_vertical.pack(side=RIGHT, fill=Y)

        self.Student_Record1.config(yscrollcommand=self.scroll_vertical.set)
        self.Student_Record1.config(xscrollcommand=self.scroll_horizontal.set)

        self.scroll_horizontal.config(command=self.Student_Record1.xview)
        self.scroll_vertical.config(command=self.Student_Record1.yview)

        self.Student_Record1['show'] = 'headings'
        self.Student_Record1.column("Course Code", anchor=CENTER, stretch=NO, width=150)
        self.Student_Record1.column("Course", anchor=CENTER, stretch=NO, width=555)

        self.Student_Record1.heading("Course Code", text="Course Code")
        self.Student_Record1.heading("Course", text="Course")

        self.Student_Record1.pack(fill=BOTH, expand=True)
        self.Student_Record1.bind("<ButtonRelease-1>", self.get_course)
        self.fetch_courses()

    def adding_courses(self):
        self.courses_add()
        self.second_window = Toplevel(root)
        self.second_window.title("Adding Courses...")
        self.second_window.resizable(False, False)
        self.second_window.geometry('900x100')

        self.Second_Frame = Frame(self.second_window, bd=2, relief=RIDGE, bg='#f1e2df')
        self.Second_Frame.place(width=899, height=99)

        self.Label_course_code = Label(self.Second_Frame, text='Course Code:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_course_code.grid(row=1, column=0, pady=10, padx=20, sticky='w')
        self.Label_course_code_entry = Entry(self.Second_Frame, textvariable=self.Course_code, bg='#dcdad5', font=('Lato', 10), bd=2,relief=GROOVE)
        self.Label_course_code_entry.grid(row=1, column=1, ipady=3, pady=35, padx=0, sticky='w')

        self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
        self.Label_course.grid(row=1, column=2, pady=10, padx=20, sticky='w')
        self.Label_course_entry = Entry(self.Second_Frame, textvariable=self.Course_name, bg='#dcdad5', bd=2, relief=GROOVE, font=('Lato', 10), width=40)
        self.Label_course_entry.grid(row=1, column=3, ipady=3, pady=0, padx=0, sticky='w')

        self.Add = Button(self.Second_Frame, text='Add', font=('Century Gothic', 12), command=self.add_courses,
                             bg='#fb8263', relief=GROOVE)
        self.Add.grid(row=1, column=4, padx=20)

        self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 12), command=self.clear_courses,
                            bg='#fb8263', relief=GROOVE)
        self.Clear.grid(row=1, column=5)

    def courses_add(self):
        self.Course_code.set('')
        self.Course_name.set('')

    def add_courses(self):
        if len(self.Course_code.get()) == 0 or len(self.Course_name.get()) == 0:
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
            cursor = connect.cursor()
            cursor.execute("INSERT INTO courses VALUES (%s, %s)",
                               (self.Course_code.get(),
                                self.Course_name.get()))
            connect.commit()
            self.fetch_courses()
            connect.close()
            messagebox.showinfo("Success", "You added a new course!")

            self.clear()
            self.second_window.destroy()

    def updating_courses(self):
        answer = messagebox.askyesno("Update Student Data", "Do you want to update data?")
        if not answer:
            pass
        else:
            self.second_window = Toplevel(root)
            self.second_window.title("Updating Courses...")
            self.second_window.resizable(False, False)
            self.second_window.geometry('900x100')

            self.Second_Frame = Frame(self.second_window, bd=2, relief=RIDGE, bg='#f1e2df')
            self.Second_Frame.place(width=899, height=99)

            self.Label_course_code = Label(self.Second_Frame, text='Course Code:', font=('Lato', 12), fg='#333438',
                                           bg='#f1e2df')
            self.Label_course_code.grid(row=1, column=0, pady=10, padx=20, sticky='w')
            self.Label_course_code_entry = Entry(self.Second_Frame, textvariable=self.Course_code, bg='#dcdad5',
                                                 font=('Lato', 10), bd=2, relief=GROOVE)
            self.Label_course_code_entry.grid(row=1, column=1, ipady=3, pady=35, padx=0, sticky='w')

            self.Label_course = Label(self.Second_Frame, text='Course:', font=('Lato', 12), fg='#333438', bg='#f1e2df')
            self.Label_course.grid(row=1, column=2, pady=10, padx=20, sticky='w')
            self.Label_course_entry = Entry(self.Second_Frame, textvariable=self.Course_name, bg='#dcdad5', bd=2,
                                            relief=GROOVE, font=('Lato', 10), width=40)
            self.Label_course_entry.grid(row=1, column=3, ipady=3, pady=0, padx=0, sticky='w')

            self.Update = Button(self.Second_Frame, text='Update', font=('Century Gothic', 12), command=self.update_courses,
                              bg='#fb8263', relief=GROOVE)
            self.Update.grid(row=1, column=4, padx=8)

            self.Clear = Button(self.Second_Frame, text='Clear', font=('Century Gothic', 12), command=self.clear_courses,
                                bg='#fb8263', relief=GROOVE)
            self.Clear.grid(row=1, column=5)

    def update_courses(self):
        if len(self.Course_code.get()) == 0 or len(self.Course_name.get()) == 0:
            messagebox.showerror("Error", "All fields should be filled!")
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
            cursor = connect.cursor()
            cursor.execute('SET FOREIGN_KEY_CHECKS=0')
            cursor.execute(f"UPDATE courses SET course='{self.Course_name.get()}', course_code='{self.Course_code.get()}' WHERE course_code='{self.var_course}'")

            connect.commit()
            self.fetch_courses()
            self.clear()
            connect.close()
            messagebox.showinfo("Success", "You updated the record!")

            self.second_window.destroy()

            self.search_entry.delete(0, END)

    def delete_courses(self):
        answer = messagebox.askyesno("Delete data", "Do you want to delete data?")
        if not answer:
            pass
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
            cursor = connect.cursor()
            cursor.execute('SET FOREIGN_KEY_CHECKS=0')
            cursor.execute("delete from courses where Course_code=%s", self.Course_code.get())
            connect.commit()
            connect.close()
            self.fetch_courses()
            self.clear()

            messagebox.showinfo("Deleted", "Record has been deleted")

    def fetch_courses(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
        cursor = connect.cursor()
        cursor.execute("select * from courses")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record1.delete(*self.Student_Record1.get_children())
            for row in rows:
                self.Student_Record1.insert('', END, values=row)
            connect.commit()
        connect.close()

        self.search_entry1.delete(0, END)

    def fetch_data(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
        cursor = connect.cursor()
        cursor.execute("select * from students")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record.delete(*self.Student_Record.get_children())
            for row in rows:
                self.Student_Record.insert('', END, values=row)
            connect.commit()
        connect.close()

    def search_courses(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
        cursor = connect.cursor()
        cursor.execute(
            "select course_code, course from courses where course_code LIKE '%"+self.Search_course.get()+"%'  ")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record1.delete(*self.Student_Record1.get_children())
            for row in rows:
                self.Student_Record1.insert('', END, values=row)
            connect.commit()
        connect.close()

    def search(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
        cursor = connect.cursor()
        cursor.execute(
            "select * from students where " + str(self.Search_by.get()) + " Like '%" + str(self.Search.get()) + "%' ")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record.delete(*self.Student_Record.get_children())
            for row in rows:
                self.Student_Record.insert('', END, values=row)
            connect.commit()
        connect.close()

    def refresh(self):
        connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
        cursor = connect.cursor()
        cursor.execute("select * from students")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.Student_Record.delete(*self.Student_Record.get_children())
            for row in rows:
                self.Student_Record.insert('', END, values=row)
            connect.commit()
        connect.close()

        self.search_entry.delete(0, END)

    def delete(self):
        answer = messagebox.askyesno("Delete data", "Do you want to delete data?")
        if not answer:
            pass
        else:
            connect = pymysql.connect(host="localhost", user="root", password="", database="sis_v2")
            cursor = connect.cursor()
            cursor.execute("delete from students where id_number=%s", self.ID_Number.get())
            connect.commit()
            connect.close()
            self.fetch_data()
            self.clear()

            messagebox.showinfo("Deleted", "Record has been deleted")

    def clear_courses(self):
        self.Course_code.set("")
        self.Course_name.set("")

    def clear(self):
        self.ID_Number.set("")
        self.Full_Name.set("")
        self.Course.set('')
        self.Year_Level.set('')
        self.Gender.set('')

    def get_data(self, e):
        selected = self.Student_Record.focus()
        values = self.Student_Record.item(selected, 'values')

        self.var = values[0]
        self.ID_Number.set(values[0])
        self.Full_Name.set(values[1])
        self.Course.set(values[2])
        self.Year_Level.set(values[3])
        self.Gender.set(values[4])

    def get_course(self, e):
        selected = self.Student_Record1.focus()
        values = self.Student_Record1.item(selected, 'values')

        self.var_course = values[0]
        self.Course_code.set(values[0])
        self.Course_name.set(values[1])


if __name__ == '__main__':
    root = Tk()
    application = SIS(root)
    root.mainloop()
