import rospy
import queue
from std_msgs.msg import String
import pyttsx3

class TextToSpeechQueueNode(object):
    def __init__(self):
        rospy.init_node('text_to_speech_queue')
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'german+f2')
        self.engine.setProperty('rate', 100)
        self.engine.setProperty('volume', 1.0)
        self.engine.connect('started-utterance', self.on_start)
    

        self.output_queue = queue.Queue()
        self.string_subscriber = rospy.Subscriber('/tts/speech', String, self.string_callback)

    def on_start(self, name):
        print(f"Started utterance '{name}'")
    
    def string_callback(self, data):
        self.output_queue.put(data.data)

    def run(self):
        print("Text to speech node started")
        while not rospy.is_shutdown():
            try:
                message = self.output_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue

            print(f"Text to speech: {message}")
            self.engine.say(message, message)
            self.engine.runAndWait()
            rospy.sleep(2)



if __name__ == '__main__':
    try:
        node = TextToSpeechQueueNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
