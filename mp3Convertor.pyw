import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import HORIZONTAL
from tkinter.ttk import *
import subprocess as sp

# create the class
class App:
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.file_name = tk.StringVar()
        self.file_whole = tk.StringVar()

        ask_filename_frame = tk.Frame(padx=5, pady=5)
        ask_filename_frame.pack(side="top")
        self.ask_filename_label = tk.Label(ask_filename_frame, text="Input sermon file:")
        self.ask_filename_label.pack(side="left",)
        self.display_filename = tk.Label(ask_filename_frame, text="", width=30)
        self.display_filename.pack(side="right")
        
        self.bottom_frame = tk.Frame(padx=5, pady=5)
        self.bottom_frame.pack(side="bottom")
        self.open_button = tk.Button(self.bottom_frame, text="Open wave file to convert", command=self.select_file)
        self.open_button.pack(side="left")

    def select_file(self):
        filename = fd.askopenfilename(
            title="Open sermon file",
            filetypes=[("Wave files","*.wav")],
            initialdir=os.getcwd()
        )
        self.file_name.set(filename)
        self.file_whole.set(os.path.dirname(filename))
        self.display_filename['text'] = os.path.basename(filename)
        self.open_button.destroy()
        self.convert_button = tk.Button(self.bottom_frame, text="Convert file to mp3", command=self.convert_file)
        self.convert_button.pack(padx=5, pady=5, side="left")

    def convert_file(self):
        #self.convert_button.pack(side="left")
        self.convert_button.destroy()
        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.close_program)
        self.exit_button.pack(side="left", padx=5, pady=5)
        self.pb = Progressbar(self.bottom_frame, orient=HORIZONTAL,length=100, mode="determinate")
        self.pb.pack(side="left", pady=5, padx=5)

        export_filename = self.file_whole.get() + "/" + os.path.basename(self.file_name.get())[:-4] + ".mp3"
        # The following execubale path is specifically for a Linux OS:
        # convert_process = sp.Popen(["/usr/bin/lame", "-b 16k", self.file_name.get(), export_filename])
        # The following execubale path is specifically for a Windows OS:
        convert_process = sp.Popen(["C:\Program Files (x86)\Lame For Audacity\lame.exe", "-b 32k", self.file_name.get(), export_filename])
        convert_process.communicate(timeout=15)
        self.pb.start()
    
        def poller():
            if convert_process.poll() is None:
                self.pb.after(100, poller)
            else:
                self.pb.stop()
                tk.messagebox.showinfo(title="Conversion Status", message="File conversion completed! Click exit to end program!")
                self.pb.destroy()

        self.pb.after(100, poller)

    def close_program(self):
        root.destroy()

    def start(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.title("Sermon Convertor")
    root.iconphoto(True, tk.PhotoImage(file="convert.png"))
    root.resizable(True, True)

    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # print("Width",windowWidth,"Height",windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))

    #root.geometry('300x100')
    app.start()