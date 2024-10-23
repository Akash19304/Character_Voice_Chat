from elevenlabs import stream, Voice, play, save
from elevenlabs.client import ElevenLabs
import os


try:
    api_key = os.getenv('ELEVENLABS_API_KEY')
except TypeError:
  exit("You forgot to set ELEVENLABS_API_KEY in your environment!")

class ElevenLabsManager:

    def __init__(self):
        
        self.client = ElevenLabs(
            api_key=api_key, 
            )
        all_voices = self.client.voices.get_all()
        # print(f"\nAll ElevenLabs voices: \n{all_voices}\n")
        with open('voices.txt', 'w') as file:
          file.write(f"\nAll ElevenLabs voices: \n{all_voices}\n")

    # Convert text to speech, then save it to file. Returns the file path
    def text_to_audio(self, input_text, save_as_wave=True, subdirectory=""):
        audio_saved = self.client.generate(
          text=input_text,
          voice=Voice(voice_id='lHi6ykYK8GliHo57jFwu'),
          model="eleven_monolingual_v1"
        )
        if save_as_wave:
          file_name = f"___Msg{str(hash(input_text))}.wav"
        else:
          file_name = f"___Msg{str(hash(input_text))}.mp3"
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_saved,tts_file)
        return tts_file

    # Convert text to speech, then play it out loud
    def text_to_audio_played(self, input_text):
        audio = self.client.generate(
          text=input_text,
          voice=Voice(voice_id='lHi6ykYK8GliHo57jFwu'),
          model="eleven_monolingual_v1"
        )
        play(audio)

    # Convert text to speech, then stream it out loud (don't need to wait for full speech to finish)
    def text_to_audio_streamed(self, input_text, voice):
        audio_stream = self.client.generate(
          text=input_text,
          voice=Voice(voice_id='lHi6ykYK8GliHo57jFwu'),
          model="eleven_monolingual_v1",
          stream=True
        )
        stream(audio_stream)


# TESTING 

if __name__ == '__main__':
    elevenlabs_manager = ElevenLabsManager()

#     elevenlabs_manager.text_to_audio_streamed("Streaming audio")
#     time.sleep(2)
#     elevenlabs_manager.text_to_audio_played("Played Audio")
#     time.sleep(2)
#     file_path = elevenlabs_manager.text_to_audio("Saved")
#     print("Finished with all tests")

#     time.sleep(30)