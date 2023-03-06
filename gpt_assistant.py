### USAGE ####
### ga = gpt_assistant(2) # for 2 seconds
### result = ga.run()

# Sound Recorder
import sounddevice as sd
import soundfile as sf 

# ChatGPT, Whisper
import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']


# Text to speech
from gtts import gTTS 
from gtts import gTTS

# Define the sampling rate and duration of the recording
samplerate = 44100
duration = 3  # in seconds


class gpt_assistant:
    def __init__(self, duration, tts = True, model_engine = "text-davinci-003"):
        self.duration = duration
        self.model_engine = model_engine
        self.tts = tts

    def run(self):
        try:
            # Record the audio
            recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
            # Wait for the recording to finish
            sd.wait()
            # Save the recording to a WAV file
            filename = '/var/tmp/recording.wav'
            sf.write(filename, recording, samplerate)


            file = open(filename, "rb")
            transcription = openai.Audio.transcribe("whisper-1", file)
            print("I heard: ",transcription["text"])

            # If termination command is send
            # if "stop" in transcription["text"] or "Stop" in transcription["text"] :
            #     break

            # Set up the prompt and model parameters
            prompt = transcription["text"]

            # Generate text with the OpenAI API
            response = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=1024
            )

            # Print the generated text
            print("Output: ",response.choices[0].text.strip()) 


            # Define the text to be converted to speech
            text = response.choices[0].text.strip()
            # Create a gTTS object with the text and language
            tts = gTTS(text=text, lang='en')

            # Save the speech to a file
            filename = '/var/tmp/output.wav'
            tts.save(filename)

            # Play the speech using the default media player
            if self.tts:
                os.system(f"mpg123 {filename}")
            os.system("rm ./temp/recording.wav")
            os.system("rm ./temp/output.wav")
            
            return text
            
        except Exception as e:
            print("Found an error! ", e)
            

# ga = gpt_assistant(2) # for 2 seconds
# result = ga.run()
