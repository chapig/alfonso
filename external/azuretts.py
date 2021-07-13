def audio(self, text):
        speech_key, service_region = "KEY", "REGION"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        random_f = f"{random.choice(range(1,55555555555))}.wav"
        audio_filename = random_f
        audio_output = speechsdk.audio.AudioOutputConfig(filename=audio_filename)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
        result = speech_synthesizer.speak_text_async(text).get()
        return random_f 
  
def get_token(self):
      fetch_token_url = "FETCH_TOKEN_URL"
      headers = {
          'Ocp-Apim-Subscription-Key': 'KEY'
      }
      response = requests.post(fetch_token_url, headers=headers)
      self.access_token = str(response.text)

def save_audio(self, text_audio):
    try:
        self.get_token()
        base_url = 'URL'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
              'Authorization': 'Bearer ' + self.access_token,
              'Content-Type': 'application/ssml+xml',
              'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
              'User-Agent': 'YOUR_RESOURCE_NAME'
          }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
              'name', 'Microsoft Server Speech Text to Speech Voice (es-MX, DaliaNeural)')
        voice.text = text_audio
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)

        if response.status_code == 200:
            audio_name = 'sample-' + self.timestr + '.wav'
            with open(audio_name, 'wb') as audio:
                audio.write(response.content)
        return audio_name
    except Exception as error:
        print(error)