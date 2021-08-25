import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Start to record the audio.")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording is finished.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()














# import wave
# import pyaudio
# from array import array
# from collections import deque
# from queue import Queue, Full
# from threading import Thread


# p = pyaudio.PyAudio()

# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"

# # const values for mic streaming
# CHUNK = 1024
# BUFF = CHUNK * 10
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100

# # const valaues for silence detection
# SILENCE_THREASHOLD = 30000
# SILENCE_SECONDS = 3


# def main():
#     q = Queue()
#     Thread(target=listen, args=(q,)).start()

# # define listen function for threading
# def listen(q):
#     # open stream
#     audio = pyaudio.PyAudio()
#     stream = audio.open(
#         format=FORMAT,
#         channels=CHANNELS,
#         rate=RATE,
#         input=True,
#         input_device_index=2,
#         frames_per_buffer=CHUNK
#     )

#     # fIXME: release initial noisy data (1sec)
#     for _ in range(0, int(RATE / CHUNK)):
#         data = stream.read(CHUNK, exception_on_overflow=False)

#     is_started = False
#     vol_que = deque(maxlen=SILENCE_SECONDS)


#     print('start listening')
#     while True:
#         try:
#             # define temporary variable to store sum of volume for 1 second 
#             vol_sum = 0

#             # read data for 1 second in chunk
#             for _ in range(0, int(RATE / CHUNK)):
#                 data = stream.read(CHUNK, exception_on_overflow=False)

#                 # get max volume of chunked data and update sum of volume
#                 vol = max(array('h', data))
#                 vol_sum += vol

#                 # if status is listening, check the volume value
#                 if not is_started:
#                     if vol >= SILENCE_THREASHOLD:
#                         print('start of speech detected')
#                         print(vol)
#                         is_started = True

#                         print("Start to record the audio.")

#                         frames = []

#                         for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#                             data = stream.read(CHUNK)
#                             frames.append(data)

#                         print("Recording is finished.")

#                         stream.stop_stream()
#                         stream.close()
#                         p.terminate()

#                         wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#                         wf.setnchannels(CHANNELS)
#                         wf.setsampwidth(p.get_sample_size(FORMAT))
#                         wf.setframerate(RATE)
#                         wf.writeframes(b''.join(frames))
#                         wf.close()




#                 # if status is speech started, write data
#                 if is_started:
#                     q.put(data)

#             # if status is speech started, update volume queue and check silence
#             if is_started:
#                 vol_que.append(vol_sum / (RATE / CHUNK) < SILENCE_THREASHOLD)
#                 if len(vol_que) == SILENCE_SECONDS and all(vol_que):
#                     print('end of speech detected')
#                     break
#         except Full:
#             pass

#     # close stream
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()


# if __name__ == '__main__':
#     main()





# import pyaudio
# from array import array
# from collections import deque
# from queue import Queue, Full
# from threading import Thread

# # const values for mic streaming
# CHUNK = 1024
# BUFF = CHUNK * 10
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000

# # const valaues for silence detection
# SILENCE_THREASHOLD = 2000
# SILENCE_SECONDS = 3

# def main():
#     q = Queue()
#     Thread(target=listen, args=(q,)).start()

# # define listen function for threading
# def listen(q):
#     # open stream
#     audio = pyaudio.PyAudio()
#     stream = audio.open(
#         format=FORMAT,
#         channels=CHANNELS,
#         rate=RATE,
#         input=True,
#         input_device_index=2,
#         frames_per_buffer=CHUNK
#     )

#     # FIXME: release initial noisy data (1sec)
#     for _ in range(0, int(RATE / CHUNK)):
#         data = stream.read(CHUNK, exception_on_overflow=False)

#     is_started = False
#     vol_que = deque(maxlen=SILENCE_SECONDS)

#     print('start listening')
#     while True:
#         try:
#             # define temporary variable to store sum of volume for 1 second 
#             vol_sum = 0

#             # read data for 1 second in chunk
#             for _ in range(0, int(RATE / CHUNK)):
#                 data = stream.read(CHUNK, exception_on_overflow=False)

#                 # get max volume of chunked data and update sum of volume
#                 vol = max(array('h', data))
#                 vol_sum += vol

#                 # if status is listening, check the volume value
#                 if not is_started:
#                     if vol >= SILENCE_THREASHOLD:
#                         print('start of speech detected')
#                         is_started = True

#                 # if status is speech started, write data
#                 if is_started:
#                     q.put(data)

#             # if status is speech started, update volume queue and check silence
#             if is_started:
#                 vol_que.append(vol_sum / (RATE / CHUNK) < SILENCE_THREASHOLD)
#                 if len(vol_que) == SILENCE_SECONDS and all(vol_que):
#                     print('end of speech detected')
#                     break
#         except Full:
#             pass

#     # close stream
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()


# if __name__ == '__main__':
#     main()

















# import pyaudio
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.set_xlim((0,500))
# ax.set_ylim((0,1000))
# line, = ax.plot([], [],c='k',lw=1)

# def init():
#     line.set_data([], [])
#     return line,

# def animate(i):
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     n = len(data)
#     x = np.linspace(0,44100/2,n/2)
#     y = np.fft.fft(data)/n
#     y = np.absolute(y)
#     y = y[range(int(n/2))]
#     line.set_data(x, y)
#     return line

# CHUNK = 2000
# RATE = 44100

# p=pyaudio.PyAudio()
# stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
#               frames_per_buffer=CHUNK,input_device_index=2)

# animation = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=200, interval=10, blit=True)


# plt.show()













































# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import smtplib
# from email.mime.text import MIMEText

# # Use the application default credentials
# cred = credentials.Certificate("mykey.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()


# # get document with a know ID
# result = db.collection("setting").document("lge000325@gmail.com").get()

# if result.exists :
#     result_dict = result.to_dict()
#     print(result_dict)
#     email = (result_dict['email'])
#     print(email)
# else:
#     print(u'No such document!')








# email_from = "lge000325@gmail.com"
# email_to = "lge000325@gmail.com"
# email_subject = "안녕하세요"
# email_content = "Sending an email test"

# msg = MIMEText(email_content)
# msg['From'] = email_from
# msg['To'] = email_to
# msg['Subject'] = email_subject

# smtp = smtplib.SMTP('smtp.gmail.com', 587)
# smtp.starttls()
# smtp.login("lge000325@gmail.com", "yocloqojcsbcptgg")
# smtp.sendmail("lge000325@gmail.com","email",msg.as_string())

# print(msg.as_string())

# smtp.quit()









# import time
# import pyaudio
# import numpy as np
# import wave

# CHUNK = 2**10
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# RECORD_SECONDS = 5


# # file name
# now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = now + ".wav"

# # audio
# p=pyaudio.PyAudio()
# stream=p.open(format=pyaudio.paInt16,CHANNELS=1,rate=RATE,input=True,
#               frames_per_buffer=CHUNK,input_device_index=2)

# # 퓨리에
# while(True):
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     n = len(data)
#     y = np.fft.fft(data)/n
#     y = np.absolute(y)
#     y = y[range(int(n/2))]
#     volume = int(np.average(np.abs(data)))
#     # print(int(np.average(np.abs(data))))
#     print(y)
#     time.sleep(0.1)

#     if np.max(y) > 2000 :
#         print("* recording")
#         frames = []
#         for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#             data = stream.read(CHUNK)
#             frames.append(data)
#         print("* done recording")
#         break
#     else :
#         continue
    
# stream.stop_stream()
# stream.close()
# p.terminate()

# # save
# wf = wave.open(filename, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()





# import pyrebase
# import time
# import datetime
# import os

# config = {
#     "apiKey": "AIzaSyD0hLlsr9pYLpyaHkpzF54Ag63-ziuIHDs",
#     "authDomain": "mode-2db93.firebaseapp.com",
#     "projectId": "mode-2db93",
#     "storageBucket": "mode-2db93.appspot.com",
#     "messagingSenderId": "575221528751",
#     "appId": "1:575221528751:web:118078047fd0986de0bc5a",
#     "measurementId": "G-W52KCDVG83"
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# path_on_cloud = "Voice/" + email + filename
# path_local = filename

# storage.child(path_on_cloud).put(path_local)















