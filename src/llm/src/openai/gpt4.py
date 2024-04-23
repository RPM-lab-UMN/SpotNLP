import openai
import rospy
import rospkg
from std_msgs.msg import String
import json

def main():
    rospy.init_node('gpt4')
    client = openai.OpenAI()
    
    queue = []
    rospy.Subscriber('/speech/command', String, lambda msg: queue.append(msg.data))

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
                response = get_response()
                f.write(text + '\n---------------\n' + response + '\n')
                f.flush()
                message_list.append({ "role": "system", "content": response })
                commands = json.loads(response)["outputs"]
                for command in commands:
                    if command["command"] == "speak":
                        print(command["perameters"]["text"])
                    if command["command"] == "sit":
                        print("Now sitting")
                    if command["command"] == "stand":
                        print("Now standing")
                    if command["command"] == "follow":
                        print(command["perameters"])
                    if command["command"] == "look":
                        print(command["perameters"])



if __name__ == '__main__':
    main()