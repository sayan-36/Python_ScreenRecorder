# Importing modules
import numpy as np
import cv2
from PIL import ImageGrab
from tkinter import *
import threading
import datetime


# Initializing window
window = Tk()
window.title('Screen Recorder by DataFlair')
window.geometry('400x200')
window.resizable(width=False, height=False)
window.configure(bg='black')

frame = Frame(window)
frame.configure(bg='black')
frame.pack()


# Function display and reset time
def Display_T():
    global Recorded, Secs, Mins, Hrs
    if Recorded:
        if Secs == 60:
            Secs = 0
            Mins += 1
        elif Mins == 60:
            Mins = 0
            Hrs += 1

        TimeCounter_Label.config(text=str(Hrs) + ':' + str(Mins) + ':' + str(Secs))
        Secs += 1
        TimeCounter_Label.after(1000, Display_T)

def Resetting_T():
    global Secs, Mins, Hrs
    Secs = 0
    Mins = 0
    Hrs = 0

    Target == 'screen'


# Function to start recording

def Starts_Recording():
    global Recorded
    Recorded = not Recorded
    Resetting_T()

    Button_Rec_thread = threading.Thread(target=Recording)
    Thread_Counter = threading.Thread(target=Display_T)
    Thread_Screen = threading.Thread(target=Screen_Recording)

    if Recorded:
        Button_Rec_thread.start()
        Thread_Counter.start()
    if Target == 'screen':
        Thread_Screen.start()


# Function for screen recording
Recorded = False
Target = 'screen'
Show_Preview = True

def Screen_Recording():
    global Show_Preview, Recorded
    name = 'screen'
    Now = datetime.datetime.now()
    date = Now.strftime("%H%M%S")
    FileFormat = 'mp4'
    filename = name + str(date) + '.' + FileFormat
    FeetPerSec = 24
    Resolutions = (1366, 768)
    Thumb_Resolutions = (342, 192)

    Four_Char_Code = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(filename, Four_Char_Code, FeetPerSec, Resolutions)

    while True:
        IMG = ImageGrab.grab()
        np_IMG = np.array(IMG)
        frame = cv2.cvtColor(np_IMG, cv2.COLOR_BGR2RGB)
        writer.write(frame)
        if Show_Preview:
            Thumb = cv2.resize(frame, dsize=Thumb_Resolutions)
            cv2.imshow('Preview - Screen Recorder', Thumb)
        if cv2.waitKey(1) == 27:
            Recorded = False
            Label_Message['text'] = 'Video was saved as ' + filename
            Recording()
            break

    writer.release()
    cv2.destroyAllWindows()

# Function for recording button
def Recording():
    global Recorded
    if Recorded:
        Button_Rec['state'] = DISABLED
        Label_Message['text'] = 'Press ESC to quit.'
    else:
        Button_Rec['state'] = NORMAL



# Making labels and buttons

Button_Rec = Button(frame, text='REC', command=Starts_Recording, font=("Times new roman",30,"bold"),bg='#e50914',  activebackground='#ab070f')
Button_Rec.grid(row=20 , column=2)

TimeCounter_Label = Label(frame, text='0:0:0',font=("Times new roman",18,"bold"), bg='black', fg='white')
TimeCounter_Label.grid(row=1, column=3)

Frame_message = Frame(window)
Frame_message.configure(bg='black')
Frame_message.pack()
Label_Message = Label(Frame_message, width=3 * 14, bg='black', fg='white')
Label_Message.pack()

window.mainloop()