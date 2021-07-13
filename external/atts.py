import random

try:
    import azure.cognitiveservices.speech as speechsdk
    from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-text-to-speech-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

speech_key, service_region = "TOKEN", "LOCATION"

def speech_synthesis_with_voice(language, gender, text_to_speech):

    if language.upper() == "ES":
        language = "spanish"
    elif language.upper() == "EN":
        language = "english"
    
    gender = gender.lower()

    gender_list = {"spanish": {"male": "Microsoft Server Speech Text to Speech Voice (es-MX, JorgeNeural)", "female": "Microsoft Server Speech Text to Speech Voice (es-MX, DaliaNeural)"}, "english": {"male": "Microsoft Server Speech Text to Speech Voice (en-GB, RyanNeural)"}}

    random_file_name = str(random.choice(range(1,5000))) + ".mp3"
    file_config = speechsdk.audio.AudioOutputConfig(filename=f"{random_file_name}")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    voice = gender_list[language][gender]
    speech_config.speech_synthesis_voice_name = voice
    #speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    speech_synthesizer.speak_text_async(text_to_speech).get()
    return random_file_name
