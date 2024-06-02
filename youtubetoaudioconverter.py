from pytube import YouTube
import requests
from moviepy.editor import *
import os
from tkinter import *

def downloadYtClip(current_url: str):
    """
    Takes in the current youtube link you want to download and returns the path where you downloaded the file
    
    Args:
    current_url (str), the youtube link passed in

    Returns:
        the directory path where the video is downloaded (assuming the download goes successful)
    """
    req = requests.head(current_url, allow_redirects=True).url
    if "youtube.com" in req:
       try:
            video_to_download = YouTube(current_url)
            print("We have found your video")
       except:
            print("Video Failed, please try again!")
            return None 
       currentStream = video_to_download.streams.filter(file_extension='mp4').order_by("abr").desc().first()
       
       try:
           downloaded_file_path = currentStream.download()
           print(downloaded_file_path)
           return downloaded_file_path
       except:
           print("Video failed to download")
    else:
        print("Error youtube link is invalid")
        return None
    return

def convertToMp3(clip: str, outputPath: str):
    try:
        downloadedClip = VideoFileClip(clip)
        audioClip  = downloadedClip.audio
        audioClip.write_audiofile(outputPath, codec='libmp3lame')
        audioClip.close()
        downloadedClip.close()
    except Exception as error:
        print("Looks like you got an error", error)
    

def main():
    ##Grabs user input, which is a string and must be from the youtube site
    current_url  = str(input("Enter the youtube video you want to convert\n"))
    downloadedClip = downloadYtClip(current_url)
    print(downloadedClip)
   
    if downloadedClip != None:
        current_path = str(input("Enter the folder/directory you want to place your downloaded song into\n"))
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        dirPath = os.path.dirname(downloadedClip)
        mp3_file_path = os.path.join(dirPath, os.path.basename(downloadedClip).replace(".mp4", ".mp3"))
        convertToMp3(downloadedClip, mp3_file_path)


if __name__ in "__main__":
    main()