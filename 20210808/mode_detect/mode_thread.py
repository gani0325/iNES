from audio_struct.audio_frame import *
from firebase.firebase_thread import *
from audio.audio_generator import *
from threading import Thread, Lock, Event
import sys, os

webcam_ent = Event()

def webcam_detect(mode_ent) :
    mode_ent.wait()
    print("웹캠 찾자!!!")


    # if (cap = -1) {
    #     print("webcam detected!")

    # 웹캠 설치 코드
          # webcam_ent.set()
    # }
    # else {
    #     print("webcam not detected!")
    # }   

