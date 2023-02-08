import pyaudio, wave, sys
from tkinter import *
import tkinter as tk
import threading
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from scipy.io import wavfile
from PIL import Image, ImageTk

root = tk.Tk()
root.title("VOCA")
root.geometry("400x400")
frame_1 = tk.Frame()
frame_2 = tk.Frame()
frame_3 = tk.Frame()
frame_4 = tk.Frame()
frame_5 = tk.Frame()
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100    
WAVE_OUTPUT_FILENAME = 'audio.wav'
p = pyaudio.PyAudio()
a = True
stream = p.open(format=FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                input_device_index = 0)
frames = []
playing = True
gender = 0
var = IntVar()
predict_data = ""

def view_frame_5():
    global predict_data
    frame_4.destroy()
    print(predict_data)
    label_1 = Label(frame_5,text=predict_data)
    label_1.pack()
    frame_5.pack()
    stream.close()          
    p.terminate()  

def predict():
    global predict_data
    df = pd.read_csv("./assets/data.csv")
    X = df.drop(["Type"], axis=1)
    y = df["Type"]

    X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size=0.3, random_state=44)
    rf_model = RandomForestClassifier(n_estimators=50, random_state=44)
    rf_model.fit(X_train, y_train)
    freqrate, data = wavfile.read("audio.wav")
    mx = float(1/freqrate) * float(max(data))
    mn = float(1/freqrate) * float(min(data))
    a = float(mx)
    b = float(mn)

    # data input replace here
    new_data = [[gender,a,b]]
    # predict
    print("predict...")
    predictions = rf_model.predict(new_data)
    predict_data = predictions[0]
    print("process done..")

def view_frame_4():
    frame_3.destroy()
    label_1 = Label(frame_4,text="PROCESSING")
    label_1.pack()
    frame_4.pack()
    predict()
    btn_1 = Button(frame_4,text="Continue",command=view_frame_5)
    btn_1.pack()


def record():
    print("recording...")
    global playing
    while playing:
        data = stream.read(CHUNK)
        frames.append(data)

def stop():
    global playing
    playing = False
    print("stop...")
    stream.stop_stream()    # "Stop Audio Recording
    # stream.close()          # "Close Audio Recording
    # p.terminate()           # "Audio System Close

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    # wf.close()
    view_frame_4()


def view_frame_3():
    frame_2.destroy()
    btn_2 = Button(frame_3,text="Record", command=threading.Thread(target=record).start)
    btn_3 = Button(frame_3,text="Stop", command=stop)
    btn_2.pack()
    btn_3.pack()
    frame_3.pack()

def view_frame_2():
    frame_1.destroy()
    label_1 = tk.Label(frame_2, text="Choose Gender:")
    R2 = tk.Radiobutton(frame_2, text="Female",  variable=var, value=0)
    R1 = tk.Radiobutton(frame_2, text="Male",  variable=var, value=1)
    check = tk.Button(frame_2, text="Continue", command= view_frame_3)
    label_1.pack()   
    R1.pack()   
    R2.pack()
    check.pack()
    frame_2.pack()

load = Image.open("assets/img.jpg")
resize_image = load.resize((100, 100))
render = ImageTk.PhotoImage(resize_image)
img = Label(frame_1, image=render)
img.image = render
img.place(x=0, y=0)
label_1 = tk.Label(frame_1, text="Let's get started")
btn_1 = Button(frame_1,text="Click Here to Start", command=view_frame_2)
label_1.pack()
img.pack()
btn_1.pack()
frame_1.pack()
root.mainloop()