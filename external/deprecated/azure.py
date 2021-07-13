from azure.cognitiveservices.search.imagesearch import ImageSearchClient
from msrest.authentication import CognitiveServicesCredentials
import random
import os, requests, uuid, json
import requests
import time
from xml.etree import ElementTree


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
        self.subscription_key = 'KEY'
        self.subscription_endpoint = "ENDPOINT"
        self.img = ImageSearchClient(endpoint=self.subscription_endpoint, credentials=CognitiveServicesCredentials(self.subscription_key))
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        
    def img_url(self, search, n):
      try:
        image_results = self.img.images.search(query=search, safeSearch='Moderate')
        if image_results.value:
            maximum = len(image_results.value)
            maximum = int(maximum/2)
            first_image_result = image_results.value[n]
            return first_image_result.thumbnail_url
      except Exception as error:
        print(error)
        raise QuotaExceeded
     

    def translate(self, text, language):
      key_var_name = 'KEY'
      endpoint = 'ENDPOINT'
      
      headers = {
            'Ocp-Apim-Subscription-Key': key_var_name,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
      
      path = '/translate?api-version=3.0'
      params = f'&to={language}'
      constructed_url = endpoint + path + params

      body = [{
              'text': f'{text}'
              }]

      request = requests.post(constructed_url, headers=headers, json=body)
      response = request.json()
      return(response[0]['translations'][0]['text'])
      
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
