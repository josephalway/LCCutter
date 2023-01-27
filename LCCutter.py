"""
LCCutter is released under "The MIT License (MIT)"

Copyright © 2023 Joseph Alway

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished 
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import tkinter as tk
import random
import os
import sys


"""
This program should determine the correct alpha-numeric for a given word used as a Cutter in LC Classification.
Based off the Cutter table available from the Library of Congress website.
"""


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(sticky="ew")
        self.create_widgets()
        self.create_menus()
        self.focus_force()
        self.my_window = None
        self.my_word = None
        self.cutter_entry.focus()

        root.resizable(1, 0)

        # root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # self.grid_columnconfigure(2, weight=1)
        self.cutter_display_text.bind("<Button-3>", self.popup_menu)

        # This binds all keys to the cutter entry and runs the new cutter function every time a key is released.
        # Binding on KeyRelease updates the value of the entry widget, before running the function.
        # Binding on Key doesn't update the Entry Widget's value until after the function has run.
        # We want the entry value to include the edit, so we want the Entry widget bound on KeyRelease.
        # <KeyRelease> fixes an entire workaround that was designed to add the letter of the key press to the label.
        self.cutter_entry.bind("<KeyRelease>", self.new_cutter)

        # We hid the window as soon as we created the root.
        # It looks nicer, if you don't see the window being centered.
        # Center the Window.
        center(root)
        # Show the window. Without this, you won't see the window.
        root.attributes('-alpha', 1.0)

    def copy_to_clipboard(self):
        try:
            sel = self.cutter_display_text.get("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(sel)
        except tk.TclError:
            pass

    # Create the GUI for our IntroScreen.
    def create_widgets(self):
        self.cutter_entry_label = tk.Label(self, text='Enter a word:')
        self.cutter_entry_label.grid(sticky="nse")

        self.cutter_entry = tk.Entry(self)
        self.cutter_entry.config(width=35)
        self.cutter_entry.grid(row=0, column=1, sticky="nsew")

        # self.cutter_button = tk.Button(self, text="Create Cutter", command=self.new_cutter)
        # self.cutter_button.grid(row=0, column=2, sticky="nsew")

        self.new_cutter_label = tk.Label(self, text="Cutter:")
        self.new_cutter_label.grid(row=1, sticky="nse")

        # Use a Disabled Text Widget instead of a Label widget.
        self.cutter_display_text = tk.Text(self, height=1, width=25, state="disabled")
        self.cutter_display_text.grid(row=1, column=1, sticky="nsew")
        self.cutter_display_text.tag_configure("left", justify="left")
        self.cutter_display_text.tag_configure("color_me_red", foreground="red")
        self.cutter_display_text.tag_add("left", 1.0, "end")

        self.button = tk.Button(self, text='?', command=self.new_window)
        self.button.grid(row=1, column=2, sticky="nse")

        # Key Bindings for moving the window. Binds to the window.
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)

    def create_menus(self):
        self.my_context_menu = tk.Menu(self, tearoff=0)
        self.my_context_menu.add_command(label="copy", command=self.copy_to_clipboard)

    def popup_menu(self, event):
        # Enable the copy menu entry, if something is selected in the cutter_display_text widget.
        # Disable the copy menu entry, if there is nothing selected. Exception is caught, if there's no selection.
        try:
            self.cutter_display_text.get("sel.first", "sel.last")
            self.my_context_menu.entryconfig("copy", state="normal")
        except tk.TclError:
            self.my_context_menu.entryconfig("copy", state="disabled")
        self.my_context_menu.post(event.x_root, event.y_root)

    # This creates one instance of our InfoWindow class.
    def new_window(self):
        if self.my_window is None:
            self.update()
            x = root.winfo_rootx()
            y = root.winfo_rooty()
            height = root.winfo_height()
            # x, y, and height are in pixels. Add, subtract, divide, etc as needed to place window where you want.
            geom = "+%d+%d" % (x, y + height)
            self.my_window = InfoWindow()
            self.my_window.geometry(geom)
            # This overrides the normal delete function of a window. Make sure to destroy the related window.
            self.my_window.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
            self.my_window.focus()
        else:
            self.my_window.focus()
            pass

    # The key word event allows an event to activate the function. Such as a key press.
    def new_cutter(self, event=None):
        # Need to Figure out solution for using delete to delete a letter. Current process lets you use it, but
        # shows an error message when you press delete. Since, the display won't update unless you press another key.

        # Get the word from the cutter_entry widget.
        self.my_word = self.cutter_entry.get()
        # Binding the Entry widget to KeyRelease fixed the need for the workaround.
        # The following if statement is needed to make sure the cutter_display_text is accurate.
        # if event.char.isalpha():
        #     This workaround doesn't work, if you are deleting a character.
        #     You have to call new_cutter twice for the deleted character to disappear in the cutter_display_text.
        #     self.my_word = self.my_word + event.char
        #     pass
        # We want to ignore the BackSpace key press, so we get the cutter instead of an error displayed.
        # elif event.keysym == 'BackSpace':
        #     self.my_word = self.my_word[:-1]
        #     Fool the rest of the logic into thinking a was pressed, so it doesn't give us an error.
        #     event.char = 'a'
        # We want to ignore these key presses, so we get the cutter instead of an error displayed.
        if event.keysym in 'Shift_L,Shift_R,Caps_Lock,Left,Right,Up,Down,Cancel,End,Home,Print,Insert,Escape':
            # Fool the rest of the logic into thinking a was pressed, so it doesn't give us an error.
            event.char = 'a'
        # Clear the self.cutter_display_text widget of text.
        self.cutter_display_text.configure(state="normal")
        self.cutter_display_text.delete(1.0, tk.END)
        my_word_length = len(self.my_word)
        # Check to make sure the character entered is a letter and output an error, if not.
        if event.char.isalpha() is False and event.keysym != 'Delete' and event.keysym != 'BackSpace':
            self.cutter_display_text.insert(1.0, "Please only use letters.", "color_me_red")
            self.cutter_display_text.configure(state="disabled")
        # Display a different note regarding the usage of delete.
        # elif event.keysym == 'Delete' or event.keysym == 'BackSpace':
        #     self.cutter_display_text.insert(1.0, "Press a key to update.", "color_me_red")
        #     self.cutter_display_text.configure(state="disabled")
        # Insert the word / cutter in the self.cutter_display_text widget.
        elif my_word_length > 0 and self.my_word.isalpha():
            new_cutter = LCCutter(self.my_word)
            my_cutter = new_cutter.get_cutter()
            self.cutter_display_text.insert(1.0, my_cutter)
            self.cutter_display_text.configure(state="disabled")
        # Leave the self.cutter_display_text widget clear, if the word length is 0.
        elif my_word_length == 0:
            self.cutter_display_text.configure(state="disabled")
        # Insert an error to cover all other cases. Example, the word containing a number, but a letter was pressed.
        else:
            self.cutter_display_text.insert(1.0, "Please only use letters.", "color_me_red")
            self.cutter_display_text.configure(state="disabled")

    # Run this when we close the child window self.my_window
    def on_closing(self):
        # Destroy the child window.
        self.my_window.destroy()
        # Set our window variable back to None.
        self.my_window = None
        # You could also do anything else here that you want to happen when closing the child window.

    # Start position for Moving the Window
    def start_move(self, event):
        self.move_x = event.x
        self.move_y = event.y

    # Stop position for Moving the Window
    def stop_move(self, event):
        self.move_x = None
        self.move_y = None

    # Move the Window.
    def on_move(self, event):
        delta_x = event.x - self.move_x
        delta_y = event.y - self.move_y
        x = root.winfo_x() + delta_x
        y = root.winfo_y() + delta_y
        root.geometry("+%s+%s" % (x, y))
        return


# Like the frame, or any widget, this inherited from the parent widget
class InfoWindow(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.grid()
        self.create_widgets()
        self.focus_force()
        self.wm_attributes('-toolwindow', True)
        self.title('Information Page')
        self.resizable(0, 0)
        # Variables for moving the window.
        self.move_x = None
        self.move_y = None

    # Create your GUI for the InfoWindow.
    def create_widgets(self):
        info_label = tk.Label(self, text='This program outputs a Library of Congress Cutter Number based on the'
                                         ' LC Cutter Table. Current as of 06/13/2017.')
        info_label.grid(row=1, sticky='w')

        info_label_two = tk.Label(self, text='\n'
                                             'Instructions for use:\n'
                                             '#1 Enter a word in the box provided. '
                                             '(The cutter appears in the box labeled \"Cutter\".)\n'
                                             '#2 Highlight the portion of the cutter you want to use.\n'
                                             '#3 Right-Click the highlighted selection and click copy from the menu.\n'
                                             'Shortcut: Ctrl+C to copy.'
                                             , justify='left')
        info_label_two.grid(row=2, sticky='w')

        about_label = tk.Label(self, text='Copyright 2023 by Joseph Alway')
        about_label.grid(row=2, sticky='es')

        # Key Bindings for moving the window. Binds to the window.
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.on_move)

    # Start position for Moving the Window
    def start_move(self, event):
        self.move_x = event.x
        self.move_y = event.y

    # Stop position for Moving the Window
    def stop_move(self, event):
        self.move_x = None
        self.move_y = None

    # Move the Window.
    def on_move(self, event):
        delta_x = event.x - self.move_x
        delta_y = event.y - self.move_y
        x = self.winfo_x() + delta_x
        y = self.winfo_y() + delta_y
        self.geometry("+%s+%s" % (x, y))
        return


class LCCutter:
    def __init__(self, new_word):
        # Initialize variables
        self.word = new_word.lower()

    def get_cutter(self):
        # Check the first letter(s) of the cutter word.
        word_length = len(self.word)
        if word_length < 2:
            return "Use at least 2 letters."
        first_letter = self.word[0]
        second_letter = self.word[1]

        my_cutter = "." + first_letter
        # Determine the correct cutter based on the first letter(s)
        # Based on the LC Cutter Table as of 06/13/2017
        if first_letter in "aeiouy":
            if second_letter in "abc":
                my_cutter = my_cutter + "2"
            elif second_letter in "defghijk":
                my_cutter = my_cutter + "3"
            elif second_letter in "lm":
                my_cutter = my_cutter + "4"
            elif second_letter in "no":
                my_cutter = my_cutter + "5"
            elif second_letter in "pq":
                my_cutter = my_cutter + "6"
            elif second_letter == "r":
                my_cutter = my_cutter + "7"
            elif second_letter in "st":
                my_cutter = my_cutter + "8"
            elif second_letter in "uvwxyz":
                my_cutter = my_cutter + "9"
            else:
                pass
        elif first_letter.lower() in "bcdfghjklmnprtuvwxz":
            if second_letter in "abcd":
                my_cutter = my_cutter + "3"
            elif second_letter in "efgh":
                my_cutter = my_cutter + "4"
            elif second_letter in "ijklmn":
                my_cutter = my_cutter + "5"
            elif second_letter in "opq":
                my_cutter = my_cutter + "6"
            elif second_letter in "rst":
                my_cutter = my_cutter + "7"
            elif second_letter in "uvwx":
                my_cutter = my_cutter + "8"
            elif second_letter in "yz":
                my_cutter = my_cutter + "9"
            else:
                pass
        elif first_letter.lower() == "s":
            if second_letter in "ab":
                my_cutter = my_cutter + "2"
            elif second_letter == "c":
                if word_length < 3:
                    my_cutter = my_cutter + "3"
                else:
                    third_letter = self.word[2]
                    if third_letter in "abcdefg":
                        my_cutter = my_cutter + "2"
                    elif third_letter in "hijklmnopqrstuvwxyz":
                        my_cutter = my_cutter + "3"
            elif second_letter == "d":
                my_cutter = my_cutter + "3"
            elif second_letter in "efg":
                my_cutter = my_cutter + "4"
            elif second_letter in "hijkl":
                my_cutter = my_cutter + "5"
            elif second_letter in "mnopqrs":
                my_cutter = my_cutter + "6"
            elif second_letter == "t":
                my_cutter = my_cutter + "7"
            elif second_letter in "uv":
                my_cutter = my_cutter + "8"
            elif second_letter in "wxyz":
                my_cutter = my_cutter + "9"
            else:
                pass
        elif first_letter.lower() == "q":
            my_dict = {}
            num_start = 2
            for letter in "abcdefghijklmnopqrst":
                my_dict[letter] = num_start
                num_start += 1
            if second_letter in "abcdefghijklmnopqrst":
                my_cutter = my_cutter + str(my_dict[second_letter])
            elif second_letter in "uvwxyz":
                if word_length < 3:
                    if second_letter in "uvwx":
                        my_cutter = my_cutter + "8"
                    elif second_letter in "yz":
                        my_cutter = my_cutter + "9"
                else:
                    third_letter = self.word[2]
                    if third_letter in "abcd":
                        my_cutter = my_cutter + "3"
                    elif third_letter in "efgh":
                        my_cutter = my_cutter + "4"
                    elif third_letter in "ijklmn":
                        my_cutter = my_cutter + "5"
                    elif third_letter in "opq":
                        my_cutter = my_cutter + "6"
                    elif third_letter in "rs":
                        my_cutter = my_cutter + "7"
                    elif third_letter in "tuvwx":
                        my_cutter = my_cutter + "8"
                    elif third_letter in "yz":
                        my_cutter = my_cutter + "9"
        else:
            pass
        # Cutter Expansion.
        if self.word[:2] == "qu":
            my_string = self.word[3:]
        else:
            my_string = self.word[2:]
        for char in my_string:
            if char in "abcd":
                my_cutter = my_cutter + "3"
            elif char in "efgh":
                my_cutter = my_cutter + "4"
            elif char in "ijkl":
                my_cutter = my_cutter + "5"
            elif char in "mno":
                my_cutter = my_cutter + "6"
            elif char in "pqrs":
                my_cutter = my_cutter + "7"
            elif char in "tv":
                my_cutter = my_cutter + "8"
            elif char in "wxyz":
                my_cutter = my_cutter + "9"
            elif char in "u":
                my_cutter = my_cutter + "u"
            else:
                pass
        # Cutters shouldn't end in 1 or 0.
        if my_cutter[-1:] in "01":
            my_cutter = my_cutter + str(random.randrange(2, 9))
        return my_cutter.upper()


# Center the window specified.
def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


root = tk.Tk()
# Hide the root window, so it doesn't show up until we've centered it in the MainWindow.
root.attributes('-alpha', 0.0)
# Create an instance of our MainWindow Class.
app = MainWindow(root)
# Set the title of the root window / MainWindow.
root.title('LC Cutter Generator v.1.0.5')
# Set the icon of the root window.
root.iconbitmap(resource_path('my_icon_lettered_new.ico'))
root.mainloop()
