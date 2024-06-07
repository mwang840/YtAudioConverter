from pytube import YouTube
import requests
from moviepy.editor import *
import os
import tkinter as tk
from tkinter import ttk, filedialog


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
    """
    Takes in the current path where the downloaded clip is in and the output directory path where you want to store your mp3 file
    Converts to mp3 then stores it in the path
    """
    ##Try catch block
    try:
        #Convert the location where the downloaded file is located in
        downloadedClip = VideoFileClip(clip)
        #Grab the audio of that downloaded video file clip
        audioClip  = downloadedClip.audio
        #Writes the audio file
        audioClip.write_audiofile(outputPath, codec='libmp3lame')
        #Close the audio file and the clip
        audioClip.close()
        downloadedClip.close()
    # Raise exception error
    except Exception as error:
        print("Looks like you got an error", error)


#Where the tkinter fun begins
def main():
    
    currentFrame = tk.Tk()
    currentFrame.title("Youtube to mp3 audio converter")
    currentFrame.geometry('400x200')
    lbl = tk.Label(currentFrame, text = "Enter the youtube video you want to convert\n")
    userInputtxt = tk.Text(currentFrame, height=2, width=30)
    lbl.pack() 
    userInputtxt.pack()

    def handleTkinterInput():
        songInput = userInputtxt.get(1.0, "end-1c")
        downloadedYtClip = downloadYtClip(songInput)
        if downloadedYtClip != None:
            currentPath = filedialog.askdirectory()
            if not os.path.exists(currentPath):
                os.makedirs(currentPath)
            mp3FilePath = os.path.join(currentPath, os.path.basename(downloadedYtClip).replace(".mp4", ".mp3"))
            convertToMp3(downloadedYtClip, mp3FilePath)
    convert_button = tk.Button(currentFrame, text="Convert", command=handleTkinterInput)
    convert_button.pack()
    currentFrame.mainloop()
    convert_button.quit()
    currentFrame.quit()  
if __name__ in "__main__":
    main()