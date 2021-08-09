"""
@author: Kojungbeom
    
reference:
    https://github.com/matrix-io/odas/blob/master/demo/matrix-demos/matrix-odas.cpp
"""

import sys
import os
sys.path.append('sLocalization/models/')

from firebase.firebase_thread import *
from mode_detect.mode_thread import *
from threading import Thread, Lock, Event

from simpleNet import simpleNet, newNet
from blankNet import BlankNet
from matrix_lite import led
import time
import torch
import numpy as np
import collections
import torch.nn.functional as F

Audio_recode_ent = Event()
Webcam_recode_ent = Event()

values = np.array([0] * 7)
# amount of decrease per iteration
DECREMENT = 5

# amount of increase per estimation
INCREMENT = 20

MAX_VALUE = 200
THRESHOLD = 20
led_dict = {0:0, 1:2, 2:5, 3:8, 4:10, 5:13, 6:15}

def increase_pots(predict=None):
    """ssl network sometimes makes wrong estimation.
    This function increases the value corresponding to the index of the estimated class,
     and the decrease_pots function decreases the value of all indexes every iteration.
     This algorithm prevents errors caused by wrong estimation that sometimes occur in ssl.
    """
    everloop = ['black'] * led.length
    if predict:
        values[predict] += INCREMENT
        if values[predict] > MAX_VALUE:
            values[predict] = MAX_VALUE
        if np.max(values) > THRESHOLD:
            everloop[led_dict[np.argmax(values)]] = {'b':50}
            led.set(everloop)
        else:
            led.set(everloop)
    else:
        led.set(everloop)


def decrease_pots():
    for i in range(len(values)):
        values[i] -= DECREMENT
        if values[i] < 0:
            values[i] = 0


angles = {0:90, 1:39, 2:-12, 3:-12, 4:192, 5:192, 6:141}

def sLocalizer(audio_que, audio_ent, motor_ent, mode_audio, webcam_ent):
    """estimate the angle from multi-channel raw audio data.

    Args:
        audio_que(queue) : que containing audio frames
        motor_ent(event): event object indicate if the motor finish rotation.

    """

    print("BlankNet Thread Join...")

    # load pretrained weights
    net = BlankNet()
    net.load_state_dict(torch.load('sLocalization/weight/197.pth', map_location=torch.device('cpu')))
    net.eval()
    #time.sleep(5)
    audio_ent.wait()





    if mode_audio.isSet :
        mode_audio.wait()
        # AUDIO 크게 바꾸기
        # 쨍그랑쨍글아 쿵쿵쿵쿵

        # if audio_que > 7000 :
        #     audio_que == audio





    for frame in audio_que.queue[-1].ssl_frame:
		# preprocess multi-channel raw audio data
        t_data = torch.tensor(np.frombuffer(frame, dtype=np.int16))
        t_data = t_data.view(-1,8).view(-1,1,320,8)
        t_data = t_data.float()

        # estimate angle only the average of amplitude of raw data is higher than 200
        angle = 0 
        if torch.mean(torch.abs(t_data)) < 200:
            increase_pots()
            decrease_pots()
            continue
       
        # pick class which has the highest probability
        outputs = net(t_data)
        c_outputs = outputs.clone()
        _, pred = outputs.max(1)
        _, top1 = outputs.topk(1)
        top1_index = int(top1[0][0])

        # class 3 and 4 are treated as over 180 degrees.
        if top1_index == 3 or top1_index == 4:
            continue
        all_psb = F.softmax(c_outputs, dim=1)[0]

        # estimate angle using probability ratio of classes adjacent to top1 class
        top1_psb = all_psb[(top1_index)]
        top1_left = all_psb[(top1_index-1)%7]
        top1_right = all_psb[(top1_index+1)%7]

        top1_near, top1_near_index = \
            (top1_left, (top1_index-1)%7) if top1_left > top1_right else (top1_right, (top1_index+1)%7)
               

        ratio = [(top1_psb / (top1_psb + top1_near)),
                (top1_near / (top1_psb + top1_near))]

        angle += angles[top1_index] * ratio[0]
        angle += angles[top1_near_index] * ratio[1]
        
        # Motor can't rotate over 180 degree
        if angle > 180:
            angle = 180
        if angle < 0:
            angle = 0

        increase_pots(predict=int(pred))
        decrease_pots()
        max_index = np.argmax(values)

        if top1_index == max_index:
            audio_que.queue[-1].frame_angle = int(angle)



            if mode_audio.wait() & webcam_ent.wait() :
                print("recoidng 해라!")
            # RECODING WEBCAM!!!!!!!!!!!!
            # RECODING AUDIO!!!!!!!!!!!
                Audio_recode_ent.set()
                Webcam_recode_ent.set()

            else :
                # RECODING AUDIO!!!!!!!!!!!
                Audio_recode_ent.set()


        else:
            audio_que.queue[-1].frame_angle = None
			#print("wrong")

