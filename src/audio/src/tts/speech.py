from openai import OpenAI
from std_msgs.msg import String
import subprocess
import rospy


def main():
    rospy.init_node('Sound')
    print("Launching Sound")
    client = OpenAI()

    play_var = {"play": False}
    def callback(msg):
        print(f"Received message: {msg.data}")
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=msg.data,
        )as response:
            response.stream_to_file("/tmp/speech.mp3")
        play_var.update({"play": True})

    # ffplay -nodisp -autoexit /tmp/speech.mp3 >/dev/null 2>&1
    rospy.Subscriber('/audio/speak', String, callback)
    while not rospy.is_shutdown():
        print(play_var)
        if play_var["play"]:
            print("Playing sound")
            subprocess.run(["ffplay", "-nodisp", "-autoexit", "/tmp/speech.mp3"])
            play_var = {"play": False}
        rospy.sleep(0.5)

if __name__ == "__main__":
    main()