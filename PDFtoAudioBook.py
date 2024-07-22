from tkinter import *
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from gtts import gTTS
import os
import threading

file_location = ''


def browse_file():
    global file_location
    filetypes = (
        ('PDF files', '*.pdf'),
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    file_location = filename
    file_location_entry.delete(0, END)
    file_location_entry.insert(0, filename)


def text_to_audio():
    if file_location_entry.get():
        convert_button.config(state='disabled')
        browse_button.config(state='disabled')
        about_app.config(text='Converting PDF to Text\nPlease wait! This can take time...', fg='gold')
        threading.Thread(target=convert_process).start()
    else:
        messagebox.showwarning(title='File Not Selected', message='Please select PDF file before converting.')


def convert_process():
    pdf_to_text()
    about_app.config(text='Converting Text to Speech\nPlease Wait!, This can take more time...', fg='gold')
    f = open("pdftext.txt", "r", encoding='utf-8')
    text = f.read()
    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save("PDFtoAudio.mp3")
    about_app.config(text='Successfully Converted.', fg='gold')
    convert_button.config(state='normal')
    browse_button.config(state='normal')
    os.system("start PDFtoAudio.mp3")
    convert_button.config(state='normal')


def pdf_to_text():
    global file_location
    with open(file_location, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    with open('pdftext.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)


window = Tk()
window.config(height=800, width=1000, padx=20, pady=20, bg='black')
window.title('PDF to AudioBook')

label_fonts = ("Verdana", 14)

typing_frame = Frame(window, bg='black')
typing_frame.grid(row=0, column=0, padx=10, pady=10)

info_frame = Frame(window, bg='black')
info_frame.grid(row=0, column=1, padx=20, pady=10, sticky='n')

about_app = Label(typing_frame,
                  text='Convert PDF to AudioBook\nChoose PDF File To Convert To Audio',
                  bg='black',
                  fg='lightcyan',
                  font=("Georgia", 14)
                  )
about_app.grid(row=0, column=0, pady=(10, 5))

file_location_entry = Entry(typing_frame,
                            font=label_fonts,
                            width=80,
                            )
file_location_entry.grid(row=1, column=0, pady=(10, 5))

browse_button = Button(typing_frame,
                       text='Browse',
                       bg='black',
                       fg='mediumpurple',
                       font=label_fonts,
                       activeforeground='black',
                       activebackground='deeppink2',
                       width=10,
                       command=browse_file
                       )
browse_button.grid(row=2, column=0, pady=(20, 0), sticky='nw')

convert_button = Button(typing_frame,
                        text='Convert',
                        bg='black',
                        fg='olivedrab1',
                        font=label_fonts,
                        activeforeground='black',
                        activebackground='olivedrab1',
                        width=10,
                        command=text_to_audio
                        )
convert_button.grid(row=2, column=0, pady=(10, 10), sticky='ne')

window.mainloop()
