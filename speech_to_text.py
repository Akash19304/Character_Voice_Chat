import time
import speech_recognition as sr
import keyboard
from rich import print

class SpeechToTextManager:
    recognizer = None
    mic = None

    def __init__(self):
        # Initialize recognizer and microphone
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def speechtotext_from_mic(self):
        print("[yellow]Speak into your microphone.")
        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                print("Processing your speech...")
                text_result = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text_result}")
                return text_result
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def speechtotext_from_file(self, filename):
        print("Listening to the file")
        try:
            with sr.AudioFile(filename) as source:
                audio = self.recognizer.record(source)
                text_result = self.recognizer.recognize_google(audio)
                print(f"Recognized: \n {text_result}")
                return text_result
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def speechtotext_from_file_continuous(self, filename):
        print("Processing file for continuous recognition")
        all_results = []
        try:
            with sr.AudioFile(filename) as source:
                while True:
                    audio = self.recognizer.record(source, duration=10)  # Listen for 10 seconds at a time
                    try:
                        result = self.recognizer.recognize_google(audio)
                        print(f"Recognized: {result}")
                        all_results.append(result)
                    except sr.UnknownValueError:
                        break  # Stop when no more speech is detected
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        final_result = " ".join(all_results).strip()
        print(f"\n\nFinal continuous recognition result: {final_result}")
        return final_result

    def speechtotext_from_mic_continuous(self, stop_key='p'):
        print("Continuous Speech Recognition is now running, say something.")
        all_results = []
        done = False

        def handle_audio():
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while not done:
                    print("Listening for speech...")
                    audio = self.recognizer.listen(source)
                    try:
                        result = self.recognizer.recognize_google(audio)
                        print(f"Recognized: {result}")
                        all_results.append(result)
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")

        # Start continuous recognition in a loop until stop_key is pressed
        while not done:
            if keyboard.read_key() == stop_key:
                print("Ending continuous recognition")
                done = True
                break
            else:
                handle_audio()

        final_result = " ".join(all_results).strip()
        print(f"\n\nHere's the result from continuous recognition:\n\n{final_result}\n\n")
        return final_result


# Tests
if __name__ == '__main__':
    TEST_FILE = "test_audio.wav"
    
    speechtotext_manager = SpeechToTextManager()

    while True:
        # Uncomment the method you'd like to test
        result = speechtotext_manager.speechtotext_from_mic()
        # result = speechtotext_manager.speechtotext_from_file(TEST_FILE)
        # result = speechtotext_manager.speechtotext_from_file_continuous(TEST_FILE)
        # result = speechtotext_manager.speechtotext_from_mic_continuous()
        print(f"\n\nFinal result:\n{result}")
        time.sleep(60)
