import requests as r
import sys
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import subprocess
import glob
import io

GLOBAL_TEMP_DIR = './'

def get_episodes():
    pass

def serverless_function(config):

    print("*************************************************")
    print("* Podcast Analysis Run ")
    print("*************************************************")

    episodes = r.get("https://www.podomatic.com/v2/podcasts/3385992/episodes")
    latest_episode = episodes.json()['episodes'][0]
    #print(latest_episode)

    print("*************************************************")
    print("* Podcast Information ")
    print("* Title: {}".format(latest_episode['title']))
    print("* Published Date: {}".format(latest_episode['published_datetime']))
    print("* Media URL: {}".format(latest_episode['media_url']))
    print("*************************************************")

    run_analysis = input("* Process this episode? Type 'yes' to continue: ")
    if run_analysis != 'yes':
        print("*************************************************")
        print("* Terminating Podcast Analysis Run ")
        print("*************************************************")
        sys.exit(0)
    
    write_location = GLOBAL_TEMP_DIR + 'tmp/%03d.flac'
#    subprocess.run(['wget', '-O', "{}web/podcast.mp3".format(GLOBAL_TEMP_DIR), latest_episode['media_url']])    
#    subprocess.run(['ffmpeg', '-i', "{}web/podcast.mp3".format(GLOBAL_TEMP_DIR), '-ar', '16000','-ac', '1', "{}web/podcast_mono.wav".format(GLOBAL_TEMP_DIR)])

    client = speech.SpeechClient()
    # output_files = glob.glob("{}tmp/*.wav".format(GLOBAL_TEMP_DIR))
    # for snippet in output_files:
    #     with io.open(snippet, 'rb') as audio_file:
    #         #content = audio_file.read()
    
    audio = types.RecognitionAudio(uri="gs://trvia_podcasts/podcast_mono.wav")
        
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code='en-US'
    )

    response = client.long_running_recognize(config, audio)

    result = response.result(timeout=500)

    transcript = ""

    for item in result.results:
        transcript += item.alternatives[0].transcript
    
    print(transcript)



if __name__ == '__main__':
    serverless_function("null")
