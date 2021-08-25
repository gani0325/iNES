


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import smtplib
from email.mime.text import MIMEText

# Use the application default credentials
cred = credentials.Certificate("mykey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


# get document with a know ID
result = db.collection("setting").document("lge000325@gmail.com").get()

if result.exists :
    result_dict = result.to_dict()
    print(result_dict)
    email = (result_dict['email'])
    print(email)
else:
    print(u'No such document!')












import pyrebase
import time
import datetime
import os
import pyaudio
import numpy as np
import wave

CHUNK = 2**10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


# file name
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = now + ".wav"

# audio
p=pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# 퓨리에
while(True):
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    n = len(data)
    y = np.fft.fft(data)/n
    y = np.absolute(y)
    y = y[range(int(n/2))]
    volume = int(np.average(np.abs(data)))
    # print(int(np.average(np.abs(data))))
    print(y)
    time.sleep(0.1)

    if np.max(y) > 50 :
        print("* recording")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("* done recording")
        break
    else :
        continue
    
stream.stop_stream()
stream.close()
p.terminate()

# save
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()







config = {
    "apiKey": "AIzaSyD0hLlsr9pYLpyaHkpzF54Ag63-ziuIHDs",
    "authDomain": "mode-2db93.firebaseapp.com",
    "databaseURL" : "https://mode-2db93-default-rtdb.firebaseio.com",
    "projectId": "mode-2db93",
    "storageBucket": "mode-2db93.appspot.com",
    "messagingSenderId": "575221528751",
    "appId": "1:575221528751:web:118078047fd0986de0bc5a",
    "measurementId": "G-W52KCDVG83"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

path_on_cloud = "Audios/" + email + "/" + filename


storage.child(path_on_cloud).put(filename)
print("upload")

url = storage.child(path_on_cloud).get_url(filename)
print("download")








email_from = "lge000325@gmail.com"
email_to = email
email_subject = "Security 알림!"
email_content = url

msg = MIMEText(email_content)
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = email_subject

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login("lge000325@gmail.com", "yocloqojcsbcptgg")
smtp.sendmail("lge000325@gmail.com", email, msg.as_string())

print(msg.as_string())

smtp.quit()






