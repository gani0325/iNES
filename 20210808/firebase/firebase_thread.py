"""
@author: Google
    Edited by Jihwan
    
reference
"""

from mode_detect.mode_thread import *
from sLocalization.ssl_thread import *

from threading import Thread, Lock, Event
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import collections
import time
import pyrebase

update_ent = Event()
mode_ent = Event()
mode_audio = Event()


tri_deq = collections.deque()
mode_deq = collections.deque()

def get_command_thread(ent, to_td_deq, email_deq, mode_ent) :
    # condition
    #
    ent.wait()
    email_id = email_deq.pop()
    doc_ref = get_doc_ref(email_id)
    doc_watch = doc_ref.on_snapshot(on_snapshot)
    while True:
        if update_ent.isSet():
            print("update_ent is set!")
            new_trigger = tri_deq.popleft()
            to_td_deq.append(new_trigger)
            update_ent.clear()
        else:
            time.sleep(2)
        if mode_ent.isSet():
            if mode_deq == "security" :
                print("security mode!")
                webcam_detect(mode_ent)
                mode_audio.set()
                print("webcam 유무 탐지 시작!")
            else :
                print("normal mode!")
                mode_ent.clear()

def get_doc_ref(email_id):
    """
    initialize Firebase Admin SDK
    set return value as user's document root
    """
    cred = credentials.Certificate("firebase/cred/alpha.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db.collection(u'setting').document(email_id)

def on_snapshot(doc_snapshot, changes, read_time):
    """
    Create a callback on_snapshot function to capture changes
    """
    pre_command = ""
    pre_mode = ""
    for doc in doc_snapshot:
        cmd_txt = doc.to_dict()["Command_text"]
        cmd_mode = doc.to_dict()["Mode"]

        if pre_mode != cmd_mode :
            print("Mode changed")
            mode_deq.append(cmd_mode)
            mode_ent.set()
        
        print(f'Command changed : {cmd_txt}')
        tri_deq.append(cmd_txt)
        update_ent.set()


def recording(Audio_recode_ent, Webcam_recode_ent) :
    Audio_recode_ent.wait()
    Webcam_recode_ent.wait()

    # audio 업로드
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    path_on_cloud = "Voices/test/test_eddy.wav" # 업로드
    path_local = "test_eddy.wav"

    files = storage.list_files()    # 다운로드
    for files in files :            # storage에 있는 파일 목록 가져오기
        print(storage.child(file.name).get_url(None))


    # webcam 업로드

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~