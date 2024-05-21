import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

import rospy
from std_msgs.msg import String


def main():
    rospy.init_node('whisper_transcribe')
    pub = rospy.Publisher('/speech/command', String, queue_size=10)
    phrase_time = None
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = 400
    recorder.dynamic_energy_threshold = False
    # recorder.dynamic_energy_threshold = True

    # mic_name = "default"
    mic_name = "sysdefault"
    # mic_name = "list"
    # mic_name = "PowerConf S3"
    print("Available microphone devices are: ")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone with name \"{name}\" found")
    exit()
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if mic_name in name:
            print(f"Microphone with name \"{name}\" found")
            source = sr.Microphone(sample_rate=16000, device_index=index)
            break

    model = "medium" + ".en"
    print("Loading model...")
    audio_model = whisper.load_model(model)
    print("Model loaded.\n")
    record_timeout = 2
    phrase_timeout = 4
    transcription = ['']

    print(source)
    # Test the microphone.
    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)
    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                phrase_time = now
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()
                if phrase_complete:
                    transcription.append(text)
                    # pub.publish(text)
                    print(f"Received: {text}")
                    if "spot" in text.lower():
                        pub.publish(text)
                        print(f"Published: {text}")
                    # pub.publish(text)
                else:
                    transcription[-1] = text
                # os.system('cls' if os.name=='nt' else 'clear')
                # for line in transcription:
                #     print(line)
                # Flush stdout.
                # print('', end='', flush=True)
            else:
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)


if __name__ == "__main__":
    main()