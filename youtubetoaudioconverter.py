from pytube import YouTube
import requests
from moviepy.editor import *
import os

def downloadYtClip(current_url: str):
    req = requests.head(current_url, allow_redirects=True).url
    if "youtube.com" in req:
       try:
            video_to_download = YouTube(current_url)
            print("We have found your video")
       except:
            print("Video Failed, please try again!")
            return None
       currentStream = video_to_download.streams.get_highest_resolution()
       
       try:
           downloaded_file_path = currentStream.download()
           return downloaded_file_path
       except:
           print("Video failed to download")
    else:
        print("Error youtube link is invalid")
        return None
    return

def convertToMp3(clip: str, outputPath: str):
    downloadedClip = VideoFileClip(clip)
    audioClip  = downloadedClip.audio
    audioClip.write_audiofile(clip, codec='libmp3lame')
    audioClip.close()
    downloadedClip.close()
    

def main():
    ##Grabs user input, which is a string and must be from the youtube site
    current_url  = "https://www.youtube.com/watch?v=b-ys7ZMn6II"
    current_path = downloadYtClip(current_url)
    if current_path:
        mp3_file_path = current_path.replace(".mp4", ".mp3")
        convertToMp3(current_path, mp3_file_path)
        print(f"MP3 file saved to {mp3_file_path}")


if __name__ in "__main__":
    main()