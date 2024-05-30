import tkinter as tk
import rospy
from std_msgs.msg import String

def main():
    rospy.init_node("VisualizeText")
    # window size: 80% of the screen width, 50% of the screen height
    window = tk.Tk()
    # windll.shcore.SetProcessDpiAwareness(1)
    window.title("Spot")
    window.geometry("2300x1100")

    # Add two text boxes, side by side with titles on top, taking up the full window width and height (minus padding), text size 40, titles: Input text, Output text:
    # input_text = tk.Text(window, height=10, width=50, font=("Helvetica", 60))
    # input_text.pack(side=tk.LEFT, padx=20, pady=20)
    # input_text.insert(tk.END, "Input text: ")

    # output_text = tk.Text(window, height=10, width=50, font=("Helvetica", 60))
    # output_text.pack(side=tk.RIGHT, padx=20, pady=20)
    # output_text.insert(tk.END, "Output text: ")

    # Add two text boxes, on top of each other, taking up the full window width and height (minus padding), text size 40, titles: Input text, Output text:
    input_text = tk.Text(window, height=5, width=50, font=("Times", 70))
    input_text.pack(side=tk.TOP, padx=20, pady=20)
    input_text.insert(tk.END, "Input text: ")
    
    output_text = tk.Text(window, height=5, width=50, font=("Times", 70))
    output_text.pack(side=tk.BOTTOM, padx=20, pady=20)
    output_text.insert(tk.END, "Output text: ")




    inputs = []
    outputs = []
    rospy.Subscriber('/audio/speak', String, lambda msg: outputs.append(msg.data))
    rospy.Subscriber('/speech/command_pre', String, lambda msg: inputs.append(msg.data))

    while rospy.is_shutdown() is False:
        if len(inputs) > 0:
            input_text.delete(1.0, tk.END)
            input_text.insert(tk.END, "Input text: " + inputs.pop(0))
        if len(outputs) > 0:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Output text: " + outputs.pop(0)) 
        window.update_idletasks()




if __name__ == "__main__":
    main()