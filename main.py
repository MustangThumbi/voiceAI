from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()


speaker = tts.init()
speaker.setProperty('rate',150)

def create_note():
    global recognizer

    speaker.say("what do you want to your note?")
    speaker.runAwait()

    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                note= recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("choose a file name")
                speaker.runAwait()
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, 'w') as f:
                f.write(note)
                f.write("\n")

                done = True
                speaker.say(f"I successfully created the note{filename}")
                speaker.runAwait()

        except speech_recognition.UnknownValueError:
            recognizer= speech_recognition.Recognizer()
            speaker.say("Come again please")
            speaker.runAwait()

# mappings = {'greeting': some_funtion}
# def add_todo():
#     global recognizer
#
#     speaker.say("What do you want to add to your todo?")
#     speaker.runAwait()
#
#     done= False
#     while not done:
#         try:
#             with speech_recognition.Microphone() as mic:
#
#                 recognizer.adjust_for_ambient_noise(mic, duration=0.2)
#                 audio = recognizer.listen(mic)
#
#                 item = recognizer.recognize_google(audio)
#                 item = item.lower()
#
#                 todo_list.append(item)
#                 done = True
#
#                 speaker.say(f"I added {item} to the to do list" )
#                 speaker.runAwait()
#         except speech_recognition.UnknownValueError:
#             recognizer= speech_recognition.Recognizer()
#             speaker.say(" I didnt understand. Please try again")
#             speaker.runAwait()


# def show_todos():
#     speaker.say("The items on your to do list are the following")
#     for item in todo_list:
#         speaker.say(item)
#         speaker.runAwait()

def hello():
    speaker.say("Hello what can I do for you?")
    speaker.runAwait()

def quit():
    speaker.say("Bye")
    speaker.runAwait()
    sys.exit(0)

mappings ={
    "greetings": hello,
    "create_note":create_note,
    # "add_todo": add_todo,
    # "show_todos": show_todos,
    "exit": quit,
}





assistant= GenericAssistant('intents.json', intents_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
# assistant.request("How are you")