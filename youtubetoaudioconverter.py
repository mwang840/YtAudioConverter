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
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
        
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

def downloadAsWav(ytLink: str):
    """
    Takes in the current youtube link you want to download, downloads it as an mp3 file and returns the path where you downloaded the file
    
    Args:
    current_url (str), the youtube link passed in

    """

    req = requests.head(ytLink, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}).url
    if "youtube.com" in req:
        try:
            ytdl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
    }
            '''
            Create a YoutubeDL object with the given options passed in, extract the information about the link
            and then prepares the output file with the output file name as an .mp3 file
            '''
            with YoutubeDL(ytdl_options) as ydl:
                current_file = ydl.extract_info(ytLink)
                ytFileName = ydl.prepare_filename(current_file).replace(".webm", ".wav").replace(".m4a", ".wav")
                return ytFileName
        except Exception as e:
            print(f"Video download failed: {e}")
            return None
            '''
            Otherwise it fails to download and returns a 500 error
            '''
        except:
                print("Video Failed, please try again!")
                return "Downloading video failed"
    return


def saveMp3Path(path: str, output: str):
     """
    Converts the downloaded clip to MP3 format and saves it to the specified output path.
    
    Args:
    path (str): The path to the downloaded video clip
    output (str): The path to save the converted MP3 file
    """
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
     return

def saveWavPath(path: str, output: str):
     """
    Converts the downloaded clip to wav format and saves it to the specified output path.
    
    Args:
    clip (str): The path to the downloaded video clip
    outputPath (str): The path to save the converted wav file
    """
     try:
        downloadedClip = VideoFileClip(path)
        audioClip = downloadedClip.audio
        # Writes the audio file - WAV doesn't need a codec specification
        audioClip.write_audiofile(output)
        audioClip.close()
        downloadedClip.close()
     except Exception as error:
        print("Error in convertToWav:", error)
        if 'downloadedClip' in locals():
            downloadedClip.close()
        if 'audioClip' in locals():
            audioClip.close()
     return

def main():
    #Setting up the GUI
    currentFrame = tk.Tk()
    currentFrame.title("YouTube Audio Converter")
    currentFrame.geometry('500x300')
    currentFrame.configure(bg="lightblue")

    #Configuring the UI
    currentFrame.columnconfigure(0, weight=1)
    currentFrame.columnconfigure(1, weight=1)
    currentFrame.rowconfigure(0, weight=1)
    currentFrame.rowconfigure(1, weight=1)
    currentFrame.rowconfigure(2, weight=1)
    lbl = tk.Label(currentFrame, font=("Arial", 15, "italic"), text = "Enter the youtube video you want to convert.\n NOTE it has to be a youtube url.\n", foreground="dark orange", bg="lightblue")
    userInputtxt = tk.Text(currentFrame, height=1, width=25)
    lbl.grid(row=0, column=0, columnspan=2, pady=1, sticky="nsew")
    userInputtxt = tk.Text(currentFrame, height=1, width=60)
    userInputtxt.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky="n")

    def handleTkinterMp3Input():
         """
         A function to handle whether the file that wants to be converted is in mp3 format
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
    
    def handleTkinterWavInput():
            """
            A function to handle whether the file that wants to be converted is in wav format
            Asks input from the tkinter
            """
            songInput = userInputtxt.get(1.0, "end-1c")
            downloadYtWavClip = downloadAsWav(songInput)
            if downloadYtWavClip != None:
                currentPath = filedialog.askdirectory()
                if not os.path.exists(currentPath):
                    os.makedirs(currentPath)
                destinationPath = os.path.join(currentPath, os.path.basename(downloadYtWavClip))
                if os.path.exists(downloadYtWavClip):
                    os.rename(downloadYtWavClip, destinationPath)
                    print(f"File saved to: {destinationPath}")
                else:
                    print(f"Source file not found: {downloadYtWavClip}")

    convert_to_mp3_button = tk.Button(currentFrame, text="Convert to Mp3🎵", command=handleTkinterMp3Input, bg="lightblue")
    convert_to_mp3_button.place(x=500, y=130)
    convert_to_mp3_button.grid(row=2, column=0, padx=25, pady=25, sticky="ne")
    handleTkinterWavInputButton = tk.Button(currentFrame, text="Convert to Wav〰", command=handleTkinterWavInput, bg="lightblue")
    handleTkinterWavInputButton.place(x=700, y=130)
    handleTkinterWavInputButton.grid(row=2, column=1, padx=25, pady=25, sticky="nw")
    currentFrame.mainloop()

if __name__ in "__main__":
     main()