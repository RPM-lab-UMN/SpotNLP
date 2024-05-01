import openai
import rospy
import rospkg
from std_msgs.msg import String, Bool, Float32, Int32
import json

def main():
    rospy.init_node('gpt4')
    client = openai.OpenAI()
    
    queue = []
    rospy.Subscriber('/speech/command', String, lambda msg: queue.append(msg.data))

    pub_camera_enable = rospy.Publisher('/camera/pub_enable', Bool, queue_size=10)
    pub_reset_xmem = rospy.Publisher('/xmem/reset', Bool, queue_size=10)
    pub_movement_mode = rospy.Publisher('/movement/mode', String, queue_size=10)
    pub_fan_power = rospy.Publisher('/movement/fan_power', Int32, queue_size=10)
    pub_speak = rospy.Publisher('/audio/speak', String, queue_size=10)
    pub_graph_nav_record_start = rospy.Publisher('/movement/graph_nav_record_start', Bool, queue_size=10)
    pub_graph_nav_record_stop = rospy.Publisher('/movement/graph_nav_record_stop', Bool, queue_size=10)
    pub_graph_nav_download = rospy.Publisher('/movement/graph_nav_download', String, queue_size=10)
    pub_graph_nav_clear = rospy.Publisher('/movement/graph_nav_clear', Bool, queue_size=10)
    pub_graph_nav_add_waypoint = rospy.Publisher('/movement/graph_nav_add_waypoint', String, queue_size=10)

    path = rospkg.RosPack().get_path('llm') + '/prompts'
    role = open(path + '/prompt.txt').read()
    actions = open(path + '/actions.json').read()
    outputs = open(path + '/outputs.json').read()
    role = role.replace('__actions__', actions)
    role = role.replace('__outputs__', outputs)
    # print(role)

    user_input = open(path + '/user_input.json').read()

    message_list = [
        { "role": "system", "content": role }
    ]
    def get_response():
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={ "type": "json_object" },
            messages=message_list
        )
        return response.choices[0].message.content


    with open(rospkg.RosPack().get_path('llm') + '/logs/gpt4.log', 'w') as f:
        f.write(role + '\n')
        while not rospy.is_shutdown():
            if queue:
                f.write("--------------------------------\n")
                text = user_input.replace("__message__", queue.pop(0))
                # TODO: Remove earlier messages if too many
                message_list.append({ "role": "user", "content": text }) 
                # TODO: Add system status message
                response = get_response()
                f.write(text + '\n---------------\n' + response + '\n')
                f.flush()
                message_list.append({ "role": "system", "content": response })
                commands = json.loads(response)["outputs"]


                for command in commands:
                    # Logistical commands -------------------------------------------
                    if command["command"] == "speak":
                        pub_speak.publish(command["perameters"]["text"])
                        print(command["perameters"]["text"])
                    
                    if command["command"] == "reset_follower":
                        pub_reset_xmem.publish(True)
                        print(command["perameters"])

                    if command["command"] == "fan_power":
                        pub_fan_power.publish(command["perameters"]["power"])
                        print(command["perameters"])

                    # Movement commands -------------------------------------------
                    if command["command"] == "sit":
                        pub_camera_enable.publish(False)
                        pub_movement_mode.publish("sit")
                        print("Now sitting")
                    
                    if command["command"] == "stand":
                        pub_camera_enable.publish(False)
                        pub_movement_mode.publish("stand")
                        print("Now standing")
                    
                    if command["command"] == "follow":
                        pub_camera_enable.publish(True)
                        pub_movement_mode.publish("follow")
                        print(command["perameters"])
                    
                    if command["command"] == "look":
                        pub_camera_enable.publish(True)
                        pub_movement_mode.publish("look")
                        print(command["perameters"])
                    
                    # GraphNav commands -------------------------------------------
                    if command["command"] == "graph_nav_record_start":
                        pub_graph_nav_record_start.publish(True)
                        print(command["perameters"])

                    if command["command"] == "graph_nav_record_stop":
                        pub_graph_nav_record_stop.publish(True)
                        print(command["perameters"])

                    if command["command"] == "graph_nav_download":
                        pub_graph_nav_download.publish(command["perameters"]["filename"])
                        print(command["perameters"])

                    if command["command"] == "graph_nav_clear":
                        pub_graph_nav_clear.publish(True)
                        print(command["perameters"])

                    if command["command"] == "graph_nav_add_waypoint":
                        pub_graph_nav_add_waypoint.publish(command["perameters"]["name"] + "\n" + command["perameters"]["description"])
                        print(command["perameters"])


            rospy.sleep(0.1)



if __name__ == '__main__':
    main()