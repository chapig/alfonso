from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from xml.etree import ElementTree
import time

class Error(Exception):
  """
  Base exception.
  """
  pass

class QuotaExceeded(Error):
  """
  Quota of Images exceeded.
  """
  pass

class Azure:
  
    def __init__(self):

        self.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
             
    def xml_text(self, text):

        xml = f"""
                <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
                    <voice name="es-MX-DaliaNeural"><mstts:express-as style="Empathy"><prosody rate="0%" pitch="-13%">{text}</prosody></mstts:express-as></voice>
                </speak>
            """

        with open("ssml.xml", "w") as output:
            output.write(xml)
            output.close()


    def audio_tts(self, text):

        self.speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])
        synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        ssml_string = open("ssml.xml", "r").read()
        result = synthesizer.speak_ssml_async(ssml_string).get()
        stream = AudioDataStream(result)
        stream.save_to_wav_file("/root/alfonso/ext/")
