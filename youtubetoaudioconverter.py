from yt_dlp import YoutubeDL
from tkinter import filedialog
import tkinter as tk
import os
import requests
from moviepy import VideoFileClip
def downloadAsMp3(ytLink: str):
    """
    Takes in the current youtube link you want to download, downloads it as an mp3 file and returns the path where you downloaded the file
    
    Args:
    current_url (str), the youtube link passed in

    """

    req = requests.head(ytLink, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}).url
    if "youtube.com" in req:
        try:
            ytdl_options = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s'
    }
            '''
            Create a YoutubeDL object with the given options passed in, extract the information about the link
            and then prepares the output file with the output file name as an .mp3 file
            '''
            with YoutubeDL(ytdl_options) as ydl:
                current_file = ydl.extract_info(ytLink)
                ytFileName = ydl.prepare_filename(current_file).replace(".webm", ".mp3").replace(".m4a", ".mp3")
                return ytFileName
            '''
            Otherwise it fails to download and returns a 500 error
            '''
        except:
                print("Video Failed, please try again!")
                return "Downloading video failed"
    return


def saveMp3Path(path, output):
     try:
          downloadedClip = VideoFileClip(path)
          audioClip = downloadedClip.audio
          audioClip.write_audiofile(output, codec="libmp3lame")
          audioClip.close()
          pass
     except Exception as error:
        print("Error in convertToMp3:", error)
        if 'downloadedClip' in locals():
            downloadedClip.close()
        if 'audioClip' in locals():
            audioClip.close()
     pass

def main():
    currentFrame = tk.Tk()
    currentFrame.title("Youtube to mp3 audio converter")
    currentFrame.geometry('400x200')
    lbl = tk.Label(currentFrame, text = "Enter the youtube video you want to convert.\n NOTE it has to be a youtube url.\n", foreground="red")
    userInputtxt = tk.Text(currentFrame, height=2, width=30)
    lbl.pack() 
    userInputtxt.pack()

    def handleTkinterMp3Input():
         """
         A function to handle whether the file that wants to be converted is in mp3 format or wav format
         Asks input from the tkinter
         """
         songInput = userInputtxt.get(1.0, "end-1c")
         downloadYtMp3Clip = downloadAsMp3(songInput)
         if downloadYtMp3Clip != None:
              currentPath = filedialog.askdirectory()
              if not os.path.exists(currentPath):
                 os.makedirs(currentPath)
              # Create the destination path
              destinationPath = os.path.join(currentPath, os.path.basename(downloadYtMp3Clip))
              # Move the file from Downloads to the selected directory
              if os.path.exists(downloadYtMp3Clip):
                  os.rename(downloadYtMp3Clip, destinationPath)
                  print(f"File saved to: {destinationPath}")
              else:
                  print(f"Source file not found: {downloadYtMp3Clip}")
         return

    convert_to_mp3_button = tk.Button(currentFrame, text="Convert to Mp3", command=handleTkinterMp3Input)
    convert_to_mp3_button.place(x=500, y=90)
    handleTkinterWavInputButton = tk.Button(currentFrame, text="Convert to Wav")
    handleTkinterWavInputButton.pack()
    handleTkinterWavInputButton.place(x=800, y=90)
    currentFrame.mainloop()

if __name__ in "__main__":
     main()