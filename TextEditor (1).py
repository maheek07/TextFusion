# Python 3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license()" for more information.
# >>>
from tkinter import *
from tkinter import ttk, messagebox, filedialog, colorchooser, font
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from time import strftime
import requests
from tkfontchooser import askfont
from googletrans import Translator
from PyDictionary import PyDictionary
import urllib.request
import wikipedia

class Editor:
    current_open_file = "no file"

    def __init__(self, root):
        self.root = root
        self.root.title("Project Editor" + " - " + self.current_open_file)
        self.root.geometry("1100x600")
        self.root.maxsize(1100,600)
        self.root.config(bg="black")
        self.word = IntVar()
        self.status = IntVar()
        self.language_list = ["en : English"]
        self.langu_list = []
        self.lang_add = StringVar()
        self.translation_text = StringVar()
        self.translate_text = StringVar()
        self.dict_text = StringVar()
        # self.close_btn_img = PhotoImage(file="http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris3_blue.png")

        self.text_area_color = "white"
        self.text_area_font_color = "black"
        self.search_box_color = "white"
        self.page_area_color = "white"
        self.wiki_area_color = "light blue"
        self.buttons_color = "#F0F0F0"
        self.font_color = "black"
        self.font_style = "arial"
        self.font_size = 10
        self.line_no = 0
        self.d_l = 35
        root.protocol("WM_DELETE_WINDOW", self.exit)

        self.frame = Frame(root, bd=1, highlightbackground="light blue", relief=GROOVE)
        self.frame.place(x=30, y=0, width=670, height=600)

        self.scroll_y = Scrollbar(self.frame, orient=VERTICAL)
        self.scroll_y.pack(side=RIGHT, fill=Y)

        self.txt_box = Text(self.frame, undo=TRUE, bg=self.text_area_color, fg=self.text_area_font_color,
                            insertbackground='red',
                            yscrollcommand=self.scroll_y.set)
        self.txt_box.pack(expand=TRUE, fill=BOTH)
        self.txt_box.focus_set()
        self.txt_box.configure(font=(self.font_style, self.font_size))
        self.scroll_y.config(command=self.txt_box.yview, bg="black", activebackground="yellow")

        self.numberLines = TextLineNumbers(root, width=30, bg='#313335')
        self.numberLines.attach(self.txt_box)
        self.numberLines.pack(side=LEFT, fill=Y)

        self.txt_box.bind("<Key>", self.onPressDelay)
        self.txt_box.bind("<Button-1>", self.numberLines.redraw)
        self.scroll_y.bind("<Button-1>", self.onScrollPress)
        self.txt_box.bind("<MouseWheel>", self.onPressDelay)

        menubar = Menu(root)

        filemenu = Menu(menubar, tearoff=TRUE)

        submenu = Menu(filemenu)
        submenu.add_command(label="Email                       Ctrl+E")
        submenu.add_command(label="Whatsapp               Ctrl+W", command=self.whatsapp)

        filemenu.add_command(label="New                 Ctrl+N", command=self.new_file)
        filemenu.add_command(label="Open               Ctrl+O", command=self.open_file)
        filemenu.add_command(label="Save                 Ctrl+S", command=self.save_file)
        filemenu.add_command(label="Save As..", command=self.save_as_file)
        filemenu.add_separator()
        filemenu.add_cascade(label="Share..", menu=submenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)


        editmenu = Menu(menubar, tearoff=TRUE)
        editmenu.add_command(label="Undo                 Ctrl+Z", command=self.txt_box.edit_undo)
        editmenu.add_command(label="Redo                 Ctrl+M", command=self.txt_box.edit_redo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut                    Ctrl+X", command=self.cut_text)
        editmenu.add_command(label="Copy                 Ctrl+C", command=self.copy_text)
        editmenu.add_command(label="Paste                 Ctrl+V", command=self.paste_text)
        editmenu.add_command(label="Delete                Del", command=self.delete_text)
        editmenu.add_separator()
        editmenu.add_command(label="Find..                 Ctrl+F", command=self.find_text)
        editmenu.add_command(label="Replace..           Ctrl+R", command=self.replace_text)
        editmenu.add_command(label="Go To..              Ctrl+G", command=self.go_to)
        editmenu.add_separator()
        editmenu.add_command(label="Select All           Ctrl+A", command=self.select_all)
        editmenu.add_command(label="Time/Date        Ctrl+T", command=self.time_date)
        menubar.add_cascade(label="Edit", menu=editmenu)

        formatmenu = Menu(menubar, tearoff=TRUE)
        formatmenu.add_checkbutton(label="Word Wrap", variable=self.word, command=self.word_wrap)
        formatmenu.add_command(label="Font..", command=self.fonts)
        menubar.add_cascade(label="Format", menu=formatmenu)

        viewmenu = Menu(menubar, tearoff=TRUE)
        viewmenu.add_checkbutton(label="Status Bar", variable=self.status, command=self.status_bar)
        menubar.add_cascade(label="View", menu=viewmenu)

        settingmenu = Menu(menubar, tearoff=TRUE)
        settingmenu.add_command(label="General", command=self.general)
        settingmenu.add_command(label="Languages         Ctrl+L", command=self.language)
        settingmenu.add_command(label="Color Scheme", command=self.color_scheme)
        settingmenu.add_command(label="Font", command=self.fonts)
        menubar.add_cascade(label="Settings", menu=settingmenu)

        helpmenu = Menu(menubar, tearoff=TRUE)
        helpmenu.add_command(label="About Developer", command=lambda : messagebox.showinfo('About','This is an exclusive distribution of Project Editor.\n Creator of this apllication is Meghanshu Kumrawat.\nThis was completed on 08/08/2020.\n Thanks For Using The Application.'))
        helpmenu.add_separator()
        helpmenu.add_command(label="View Help           Ctrl+H", command=lambda :messagebox.showinfo("Project Editor", "This Feature You CLicked Will Be Coming Soon,\nPlease Wait For An Update. Stay Tuned"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.pop_up = Menu(menubar, tearoff=TRUE)
        self.pop_up.add_command(label="Cut                    Ctrl+X", command=self.cut_text)
        self.pop_up.add_command(label="Copy                 Ctrl+C", command=self.copy_text)
        self.pop_up.add_command(label="Paste                 Ctrl+V", command=self.paste_text)
        self.pop_up.add_command(label="Delete                Del", command=self.delete_text)
        self.pop_up.add_separator()
        self.pop_up.add_command(label="Find..                 Ctrl+F", command=self.find_text)
        self.pop_up.add_command(label="Replace..           Ctrl+R", command=self.replace_text)
        self.pop_up.add_separator()
        self.pop_up.add_command(label="Select All           Ctrl+A", command=self.select_all)
        self.pop_up.add_command(label="Time/Date        Ctrl+T", command=self.time_date)

        root.config(menu=menubar)

        self.main_function()

    def main_function(self):
        root.bind('<Control-f>', self.find_text)
        root.bind('<Control-s>', self.save_file)
        root.bind('<Control-o>', self.open_file)
        root.bind('<Control-r>', self.replace_text)
        root.bind('<Control-a>', self.select_all)
        root.bind('<Control-n>', self.new_file)
        root.bind('<Control-d>', self.delete_text)
        root.bind('<Control-t>', self.time_date)
        root.bind('<Control-g>', self.go_to)
        root.bind('<Control-z>', self.txt_box.edit_undo)
        root.bind('<Control-m>', self.txt_box.edit_redo)
        root.bind('<Control-h>', self.about_help)
        root.bind('<Control-l>', self.language)
        root.bind('<Control-w>', self.whatsapp)
        root.bind('<Control-e>', self.email)
        root.bind('<Button-3>', self.right_click)

        self.search_txt = StringVar()
        self.lang = StringVar()
        self.chack = IntVar()
        self.text = IntVar()
        self.file = IntVar()
        self.font_size = IntVar()


        self.wiki_frame = Frame(root, bg=self.wiki_area_color)
        self.wiki_frame.place(x=710, y=0, width=390, height=600)

        Label(self.wiki_frame, bg=self.wiki_area_color, text="Search here").place(x=10, y=0)

        self.search_E = Entry(self.wiki_frame, width=61, textvariable=self.search_txt)
        self.search_E.place(x=10, y=25)

        Button(self.wiki_frame, text="search", cursor="hand2", bg=self.buttons_color, fg=self.font_color, command=self.search).place(
            x=330, y=50)
        Button(self.wiki_frame, text="open page", cursor="hand2", bg=self.buttons_color, fg=self.font_color,
               command=self.open_page).place(x=253, y=50)
        Button(self.wiki_frame, text="summary", cursor="hand2", bg=self.buttons_color, fg=self.font_color, command=self.summary).place(
            x=180, y=50)
        self.lang_box = ttk.Combobox(self.wiki_frame, state="readonly", textvariable=self.lang)
        self.lang_box.place(x=10, y=50)
        self.lang_box["values"] = self.language_list
        self.lang_box.current(0)

        self.list_frame = Frame(self.wiki_frame, bg="black")
        self.list_frame.place(x=10, y=80, width=370, height=100)
        scroll = Scrollbar(self.list_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)
        self.listbox = Listbox(self.list_frame, bg=self.search_box_color, yscrollcommand=scroll.set)
        scroll.config(command=self.listbox.yview)
        self.listbox.pack(expand=TRUE, fill=BOTH)

        self.scroll_frame = Frame(self.wiki_frame, bg="black")
        self.scroll_frame.place(x=10, y=190, width=370, height=350)
        self.wiki_text = ScrolledText(self.scroll_frame, bg=self.page_area_color)
        self.wiki_text.pack(expand=TRUE, fill=BOTH)

        self.translate_frame = Frame(root, bg="#313335")
        self.translate_frame.place(x=0, y=600, width=1100, height=50)

        Button(self.wiki_frame, text="<-open page on editor", cursor="hand2", bg=self.buttons_color, fg=self.font_color, command=self.open_page_on_editor).place(
            x=10, y=550)
        Button(self.wiki_frame, text="Translator", cursor="hand2", width=10, bg=self.buttons_color, fg=self.font_color, command=self.Translator).place(
            x=175, y=550)
        Button(self.wiki_frame, text="Dictionary", cursor="hand2", width=10, bg=self.buttons_color, fg=self.font_color, command=self.dictionary).place(
            x=290, y=550)


    def onScrollPress(self, *args):
        self.scroll_y.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scroll_y.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        root.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.txt_box.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.txt_box.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.txt_box.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.txt_box.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()

    def search(self):
        try:
            l = self.lang.get().split(":")[0]
            wikipedia.set_lang(l.strip())

            if self.search_txt.get() == "":
                messagebox.showerror("Editor", "Please fill the box!!!")
            else:
                search_result = wikipedia.search(self.search_txt.get())
                self.listbox.delete(0, END)
                for i in search_result:
                    self.listbox.insert(END, i)
                self.listbox.bind('<<ListboxSelect>>', self.active)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def active(self, e=None):
        self.search_txt.set(self.listbox.get(ANCHOR))

    def open_page(self):
        try:
            l = self.lang.get().split(":")[0]
            wikipedia.set_lang(l.strip())
            if self.search_txt.get() == "":
                messagebox.showerror("Project Editor", "Please fill the box!!!")
            else:
                search_result = wikipedia.summary(self.search_txt.get(), sentences=10)
                self.wiki_text.delete("0.1", END)
                self.wiki_text.insert(END, search_result)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def open_page_on_editor(self):
        try:
            l = self.lang.get().split(":")[0]
            wikipedia.set_lang(l.strip())
            if self.search_txt.get() == "":
                messagebox.showerror("Project Editor", "Please fill the box!!!")
            else:
                search_result = wikipedia.summary(self.search_txt.get(), sentences=10)
                if self.current_open_file == "no file":
                    self.txt_box.delete("0.1", END)
                    self.txt_box.insert(END, search_result)
                else:
                    self.save_file()
                    self.new_file()
                    self.txt_box.delete("0.1", END)
                    self.txt_box.insert(END, search_result)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def summary(self):
        try:
            l = self.lang.get().split(":")[0]
            wikipedia.set_lang(l.strip())
            if self.search_txt.get() == "":
                messagebox.showerror("Project Editor", "Please fill the box!!!")
            else:
                search_result = wikipedia.summary(self.search_txt.get(), sentences=1)
                self.wiki_text.delete("0.1", END)
                self.wiki_text.insert(END, search_result)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def save_file(self, e=None):
        if self.current_open_file == "no file":
            self.save_as_file()
        else:
            file = open(self.current_open_file, "w+")
            file.write(self.txt_box.get("0.1", END))
            file.close()

    def save_as_file(self):
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        if file is None:
            return
        text = self.txt_box.get("0.1", END)
        file.write(text)
        self.current_open_file = file.name
        file.close()
        self.root.title("Project Editor" + " - " + self.current_open_file)

    def open_file(self, e=None):
        file = filedialog.askopenfile()
        if file != None:
            self.txt_box.delete("0.1", END)
            for line in file:
                self.txt_box.insert(END, line)
                self.current_open_file = file.name
            file.close()
        self.root.title("Project Editor" + " - " + self.current_open_file)

    def new_file(self, e=None):
        self.txt_box.delete("0.1", END)
        self.current_open_file = "no file"
        self.root.title("Project Editor" + " - " + self.current_open_file)

    def copy_text(self, e=None):
        self.txt_box.clipboard_clear()
        self.txt_box.clipboard_append(self.txt_box.selection_get())
        self.translation_text.set(self.txt_box.clipboard_get())
        self.dict_text.set(self.txt_box.clipboard_get())

    def cut_text(self, e=None):
        self.copy_text()
        self.txt_box.delete("sel.first", "sel.last")

    def paste_text(self, e=None):
        self.txt_box.insert(INSERT, self.txt_box.clipboard_get())

    def delete_text(self, e=None):
        self.txt_box.delete("sel.first", "sel.last")

    def select_all(self, e=None):
        self.txt_box.tag_add("sel", "1.0", END)

    def time_date(self, e=None):
        time = datetime.now().strftime("%I:%M %p %D")
        self.txt_box.insert(INSERT, time)

    def find_text(self, e=None):
        top = Toplevel(root)
        top.geometry("400x100")
        Label(top, text="Find what..").place(x=10, y=20)
        self.edit = Entry(top, width=35)
        self.edit.place(x=80, y=20)
        self.edit.focus_set()
        Button(top, text="Find", cursor="hand2", bg=self.buttons_color,fg=self.font_color, width=10, command=self.find).place(x=310,y=16)
        Button(top, text="Cancel", cursor="hand2", bg=self.buttons_color,fg=self.font_color, width=10, command=top.destroy).place(x=310, y=56)
        Checkbutton(top, text="Match case", variable=self.chack).place(x=10, y=60)

    def find(self):
        self.txt_box.tag_remove('found', '1.0', END)
        s = self.edit.get()
        if s:
            idx = '0.1'
            while 1:
                if self.chack.get()==1:
                    self.r=0
                else:
                    self.r=1
                idx = self.txt_box.search(s, idx, nocase=self.r,
                                  stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(s))
                self.txt_box.tag_add('found', idx, lastidx)
                idx = lastidx
        self.txt_box.tag_config('found', background="blue", foreground="white")
        self.edit.focus_set()

    def replace_text(self, e=None):
        top = Toplevel(root)
        top.geometry("400x150")

        Label(top, text="Find what..").place(x=10, y=20)
        Label(top, text="Replace with..").place(x=10, y=60)
        self.edit = Entry(top, width=30)
        self.edit.place(x=100, y=20)
        self.edit.focus_set()
        self.edit2 = Entry(top, width=30)
        self.edit2.place(x=100, y=60)
        Checkbutton(top, text="Match case", variable=self.chack).place(x=10, y=100)
        Button(top, text="Find", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.find).place(x=310, y=18)
        Button(top, text="Replace All", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.findNreplace).place(x=310, y=58)
        Button(top, text="Cancel", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=top.destroy).place(x=310, y=98)

    def findNreplace(self):
        self.txt_box.tag_remove('found', '1.0', END)

        s = self.edit.get()
        r = self.edit2.get()

        if (s and r):
            idx = '1.0'
            while 1:

                idx = self.txt_box.search(s, idx, nocase=self.r,
                                  stopindex=END)
                if not idx: break

                lastidx = '% s+% dc' % (idx, len(s))

                self.txt_box.delete(idx, lastidx)
                self.txt_box.insert(idx, r)

                lastidx = '% s+% dc' % (idx, len(r))

                self.txt_box.tag_add('found', idx, lastidx)
                idx = lastidx

            self.txt_box.tag_config('found', foreground='green', background='yellow')
        self.edit.focus_set()

    def go_to(self, e=None):
        top = Toplevel(root)
        top.geometry("245x100")
        Label(top, text="Line number:").place(x=10, y=10)
        edit = Entry(top, width=37)
        edit.place(x=10, y=30)
        edit.focus_set()
        Button(top, text="Go To", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=7, command=None).place(x=100, y=60)
        Button(top, text="Cancel", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=7, command=top.destroy).place(x=175, y=60)
        messagebox.showinfo("Project Editor", "This Feature You CLicked Will Be Coming Soon,\nPlease Wait For An Update. Stay Tuned")

    def word_wrap(self):
        if self.word.get() == 1:
            self.txt_box.config(wrap=WORD)
        else:
            self.txt_box.config(wrap=None)

    def fonts(self):
        font = askfont(root)
        # font is "" if the user has cancelled
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            self.set_font(font_str)

    def set_font(self, f):
        self.txt_box.configure(font=(f))

    def status_bar(self):
        if self.status.get() == 1:
            self.frame1 = Frame(self.wiki_frame, bg="blue")
            self.frame1.place(x=0, y=580, width=390, height=20)
            self.lbl = Label(self.frame1, fg="white", bg="blue")
            self.lbl.place(x=200,y=0)
            self.internet = Label(self.frame1, fg="white", bg="blue" )
            self.internet.place(x=10, y=0)
            self.time()
        else:
            self.frame1.destroy()

    def time(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host)  # Python 3.x
            internet = 'Internet connected'
        except:
            internet = 'No internet'
        time_string = strftime('%H:%M:%S %p               %D %b')
        self.lbl.config(text=time_string)
        self.internet.config(text=internet)
        self.lbl.after(1000, self.time)

    def language(self, e=None):
        try:
            self.top_lang = Toplevel(root)
            self.top_lang.geometry("350x450")
            Label(self.top_lang, text="Add new Language").place(x=10, y=10)
            Entry(self.top_lang, width=35, textvariable=self.lang_add).place(x=10, y=40)
            Button(self.top_lang, text="Add",bg=self.buttons_color, fg=self.font_color, width=10, command=self.add_lang).place(x=250, y=36)

            list_frame1 = Frame(self.top_lang, bg="black")
            list_frame1.place(x=10, y=70, width=230, height=250)
            scroll1 = Scrollbar(list_frame1, orient=VERTICAL)
            scroll1 = Scrollbar(list_frame1, orient=VERTICAL)
            scroll1.pack(side=RIGHT, fill=Y)
            self.listbox_3 = Listbox(list_frame1, bg=self.search_box_color, yscrollcommand=scroll1.set)
            scroll1.config(command=self.listbox_3.yview)
            self.listbox_3.pack(expand=TRUE, fill=BOTH)
            self.listbox_3.bind('<<ListboxSelect>>', self.lang_active)

            for k, v in wikipedia.languages().items():
                self.langu_list.append(k+" : "+v)
            for i in self.langu_list:
                self.listbox_3.insert(END, i)

            Label(self.top_lang, text="Delete Language").place(x=10, y=350)
            self.c_box = ttk.Combobox(self.top_lang, width=32)
            self.c_box["values"] = self.language_list
            self.c_box.place(x=10, y=380)
            Button(self.top_lang, text="Delete", cursor="hand2",bg=self.buttons_color, fg=self.font_color, width=10, command=self.del_lang).place(x=250, y=380)
            Button(self.top_lang, text="Ok", cursor="hand2",bg=self.buttons_color, fg=self.font_color, width=10, command=self.top_lang.destroy).place(x=250, y=410)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def lang_active(self, e=None):
        self.lang_add.set(self.listbox_3.get(ANCHOR))

    def add_lang(self):
        self.language_list.append(self.lang_add.get())
        self.lang_box["values"] = self.language_list
        self.c_box["values"] = self.language_list

    def del_lang(self):
        self.language_list.remove(self.c_box.get())
        self.lang_box["values"] = self.language_list
        self.c_box["values"] = self.language_list

    def color_scheme(self):
        top = Toplevel(root)
        top.geometry("400x200")
        Label(top, text="Set Colours", font=("arial",10)).place(x=10, y=0)
        ttk.Separator(top).place(x=0, y=20, relwidth=1)
        Label(top, text="Text Area").place(x=10, y=30)
        Label(top, text="Text Area Font").place(x=10, y=60)
        Label(top, text="Search Box").place(x=10, y=90)
        Label(top, text="Page Area").place(x=10, y=120)
        Label(top, text="Wikipedia Area").place(x=200, y=30)
        Label(top, text="Buttons").place(x=200, y=60)
        Label(top, text="Button Fonts").place(x=200, y=90)
        Label(top, text="Translator").place(x=200, y=120)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.text_area).place(x=100, y=26)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.text_area_font).place(x=100, y=56)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.search_box).place(x=100, y=86)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.page_area).place(x=100, y=116)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.wiki_area).place(x=290, y=26)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.buttons).place(x=290, y=56)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.font_color_ch).place(x=290, y=86)
        Button(top, text="set color", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10,
               command=self.translator_color).place(x=290, y=116)
        Button(top, text="Ok", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=top.destroy).place(x=290, y=150)

    def text_area(self):
        self.text_area_color = colorchooser.askcolor()[1]
        self.txt_box.config(bg=self.text_area_color)

    def text_area_font(self):
        self.text_area_font_color = colorchooser.askcolor()[1]
        self.txt_box.config(fg=self.text_area_font_color)

    def search_box(self):
        self.search_box_color = colorchooser.askcolor()[1]
        self.listbox.config(bg=self.search_box_color)

    def page_area(self):
        self.page_area_color = colorchooser.askcolor()[1]
        self.wiki_text.config(bg=self.page_area_color)

    def wiki_area(self):
        self.wiki_area_color = colorchooser.askcolor()[1]
        self.wiki_frame.config(bg=self.wiki_area_color)

    def translator_color(self):
        color = colorchooser.askcolor()[1]
        self.translate_frame.config(bg=color)

    def buttons(self):
        msg = messagebox.askyesnocancel("Project Editor", "Please save file before change color!")
        if str(msg) == "True":
            self.save_file()
            self.buttons_color = colorchooser.askcolor()[1]
            self.current_open_file = "no file"
            self.main_function()
        elif str(msg) == "False":
            self.buttons_color = colorchooser.askcolor()[1]
            self.main_function()

    def font_color_ch(self):
        msg = messagebox.askyesnocancel("Project Editor", "Please save file before change color!")
        if str(msg) == "True":
            self.save_file()
            self.font_color = colorchooser.askcolor()[1]
            self.current_open_file = "no file"
            self.main_function()
        elif str(msg) == "False":
            self.font_color = colorchooser.askcolor()[1]
            self.main_function()

    def status_line_no(self, e=None):
        self.line_no +=1

    def general(self):
        messagebox.showinfo("Project Editor", "This Feature You CLicked Will Be Coming Soon,\nPlease Wait For An Update. Stay Tuned")
        top = Toplevel(root)
        top.geometry("500x300")
        Label(top, text="General Settings", font=("Courier 15 bold")).pack()
        ttk.Separator(top).place(x=0, y=25, relwidth=1)
        Label(top, text="Enter Text :").place(x=10, y=40)


    def about_help(self, e=None):
        pass

    def exit(self):
        msg = messagebox.askyesnocancel("Project Editor", "Do you want to save changes to Untitled?")
        if str(msg) == "True":
            self.save_file()
        elif str(msg) == "False":
            root.destroy()

    def email(self, e=None):
        pass

    def whatsapp(self, e=None):
        self.top_wp = Toplevel(root)
        self.top_wp.geometry("300x200")
        self.phone = StringVar()
        Label(self.top_wp, text="Share via Whatsapp", font=("arial", 10)).place(x=10, y=0)
        ttk.Separator(self.top_wp).place(x=0, y=20, relwidth=1)
        Label(self.top_wp, text="Phone no.").place(x=10, y=40)
        Checkbutton(self.top_wp, text="Share as Text", variable=self.text).place(x=10, y=80)
        # Checkbutton(self.top_wp, text="Share as (.txt) File", variable=self.file).place(x=10, y=120) I will create this function as soon as possible
        Entry(self.top_wp, width=30, textvariable=self.phone).place(x=90, y=40)
        Button(self.top_wp, text="Send", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.send).place(x=100, y=165)
        Button(self.top_wp, text="Cancel", cursor="hand2", bg=self.buttons_color, fg=self.font_color, width=10, command=self.top_wp.destroy).place(x=200, y=165)

    def send(self):
        import pywhatkit as kit
        import pyautogui as pag
        messagebox.showinfo("Information", "Wait a few seconds!!!\nAfter few seconds Whatsapp Web will be open. Scan bar code from your Whatsapp App and wait for a 1 minutes")
        if self.text.get() == 1:
            try:
                kit.sendwhatmsg(self.phone.get(), self.txt_box.get("0.1", END), int(datetime.now().strftime("%H")), int(datetime.now().strftime("%M"))+2)
                pag.press("enter")
            except Exception as e:
                messagebox.showerror("Error", e)

    def right_click(self, e=None):
        self.pop_up.post(e.x_root, e.y_root)

    def Translator(self):
        root.geometry("1100x650")
        root.maxsize(1100, 650)
        self.input_text = Entry(self.translate_frame, textvariable=self.translation_text, width=50)
        self.input_text.place(x=20, y=15)

        self.choose_langauge = ttk.Combobox(self.translate_frame, state='readonly',
                                            font=('arial', 10), width=10)

        self.choose_langauge['values'] = (
            'Afrikaans',
            'Albanian',
            'Arabic',
            'Armenian',
            ' Azerbaijani',
            'Basque',
            'Belarusian',
            'Bengali',
            'Bosnian',
            'Bulgarian',
            ' Catalan',
            'Cebuano',
            'Chichewa',
            'Chinese',
            'Corsican',
            'Croatian',
            ' Czech',
            'Danish',
            'Dutch',
            'English',
            'Esperanto',
            'Estonian',
            'Filipino',
            'Finnish',
            'French',
            'Frisian',
            'Galician',
            'Georgian',
            'German',
            'Greek',
            'Gujarati',
            'Haitian Creole',
            'Hausa',
            'Hawaiian',
            'Hebrew',
            'Hindi',
            'Hmong',
            'Hungarian',
            'Icelandic',
            'Igbo',
            'Indonesian',
            'Irish',
            'Italian',
            'Japanese',
            'Javanese',
            'Kannada',
            'Kazakh',
            'Khmer',
            'Kinyarwanda',
            'Korean',
            'Kurdish',
            'Kyrgyz',
            'Lao',
            'Latin',
            'Latvian',
            'Lithuanian',
            'Luxembourgish',
            'Macedonian',
            'Malagasy',
            'Malay',
            'Malayalam',
            'Maltese',
            'Maori',
            'Marathi',
            'Mongolian',
            'Myanmar',
            'Nepali',
            'Norwegian'
            'Odia',
            'Pashto',
            'Persian',
            'Polish',
            'Portuguese',
            'Punjabi',
            'Romanian',
            'Russian',
            'Samoan',
            'Scots Gaelic',
            'Serbian',
            'Sesotho',
            'Shona',
            'Sindhi',
            'Sinhala',
            'Slovak',
            'Slovenian',
            'Somali',
            'Spanish',
            'Sundanese',
            'Swahili',
            'Swedish',
            'Tajik',
            'Tamil',
            'Tatar',
            'Telugu',
            'Thai',
            'Turkish',
            'Turkmen',
            'Ukrainian',
            'Urdu',
            'Uyghur',
            'Uzbek',
            'Vietnamese',
            'Welsh',
            'Xhosa',
            'Yiddish',
            'Yoruba',
            'Zulu',
        )

        self.choose_langauge.place(x=350, y=12)
        self.choose_langauge.current(self.d_l)

        self.output_text = Entry(self.translate_frame, textvariable=self.translate_text, width=50)
        self.output_text.place(x=470, y=15)

        button = Button(self.translate_frame, text="Translate", cursor="hand2", width=10, command=self.translate)
        button.place(x=800, y=10)

        copy_button = Button(self.translate_frame, text="Copy Text", cursor="hand2", width=10, command=self.copy_text_transl)
        copy_button.place(x=900, y=10)

        close = Button(self.translate_frame, image=self.close_btn_img, cursor="hand2",  command=self.close)
        close.place(x=1080, y=5)

    def close(self):
        root.geometry("1100x600")
        root.maxsize(1100, 600)

    def translate(self):
        language_1 = self.translation_text.get()
        cl = self.choose_langauge.get()
        try:
            if language_1 == '':
                messagebox.showerror('Translator', 'please fill the box')
            else:
                translator = Translator()
                output = translator.translate(language_1, dest=cl)
                self.translate_text.set(output.text)
        except:
            messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def clear(self):
        self.input_text.delete(1.0, 'end')
        self.output_text.delete(1.0, 'end')

    def copy_text_transl(self):
        self.output_text.clipboard_clear()
        self.output_text.clipboard_append(self.translate_text.get())

    def dictionary(self):
        top = Toplevel(root)
        top.geometry("500x260")
        Label(top, text="Dictionary", font=("Courier 15 bold")).pack()
        ttk.Separator(top).place(x=0, y=25, relwidth=1)
        Label(top, text="Enter Text :").place(x=10, y=40)
        self.entry = Entry(top, textvariable=self.dict_text, width=50)
        self.entry.place(x=80, y=40)
        Button(top, text="Search", cursor="hand2", width=10, command=self.dictionary_func).place(x=400, y=37)
        Button(top, text="Insert in file", cursor="hand2", width=10, command=self.paste_dict_text).place(x=400, y=80)
        Button(top, text="......", cursor="hand2", width=10).place(x=400, y=124)
        Button(top, text="Clear", cursor="hand2", width=10, command=lambda : self.scroll_bar.delete(1.0, END)).place(x=400, y=166)
        Button(top, text="Close", cursor="hand2", width=10, command=top.destroy).place(x=400, y=210)
        Label(top, text="Result :").place(x=10, y=70)
        self.scroll_bar = ScrolledText(top)
        self.scroll_bar.place(x=80, y=70, width=310, height=170)
        self.scroll_bar.config(font=("Courier 10"))

    def dictionary_func(self):
        if self.entry.get() == "":
            messagebox.showerror("Dictionary", 'please fill the box')
        else:
            try:
                a = ''
                word1 = self.entry.get()
                dictionary = PyDictionary()
                a = dictionary.meaning(word1)
                str1 = ""
                if a is None:
                    messagebox.showerror("Dictionary", 'Not found!!!')
                else:
                    for i in a["Noun"]:
                        str1 += str(i) + " , "
                        self.scroll_bar.delete(1.0, END)
                        self.scroll_bar.insert(END, str1)
            except TypeError:
                messagebox.showerror("Project Editor", "Please check your Internet connection!!!")

    def paste_dict_text(self):
        self.txt_box.insert(INSERT, self.scroll_bar.get(1.0, END))

class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="white")

            i = self.textwidget.index("%s+1line" % i)



if __name__ == '__main__':
    root = Tk()
    obj = Editor(root)
    root.mainloop()
