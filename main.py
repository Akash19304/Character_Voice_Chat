import time
import keyboard
from rich import print
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager
from speech_to_text import SpeechToTextManager

ELEVENLABS_VOICE = "lHi6ykYK8GliHo57jFwu" # Replace this with the name of whatever voice you have created on Elevenlabs
# no change will occur on replacing this. -> not implemented yet

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()
stt_manager = SpeechToTextManager()


# change the first system message to change character
FIRST_SYSTEM_MESSAGE = {"role": "system", 
                        "content": '''
You're Professor! The mysteries of the universe are scattered across the cosmos, and it's your job to solve complex equations, lecture brilliant minds, and uncover the secrets of space and time. Ready your intellect, gather your books, and dive deep into knowledge to unlock the ultimate truths. Let’s begin!
While responding as Professor, you must obey the following rules:  
1) Provide short responses, only 1 line at most.
'''}

openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    # mic_result = input("[yellow]\nType out your next question, then hit enter: \n\n")
    mic_result = stt_manager.speechtotext_from_mic()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, False)

    audio_manager.play_audio(elevenlabs_output, True, True, True)


    print("[bright_cyan]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    