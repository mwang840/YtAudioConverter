from pytube import YouTube
import requests
def main():
    ##Grabs user input, which is a string and must be from the youtube site
    current_url  = str(input())
    print(current_url)
    req = requests.head(current_url, allow_redirects=True).url
    if "youtube.com" in req:
       try:
            video_to_download = YouTube(current_url)
            print("We have found your video")
       except:
            print("Video Failed, please try again!")
       currentStream = video_to_download.streams.get_highest_resolution()
       
       try:
           currentStream.download()
           print(type(currentStream.download()))
       except:
           print("Video failed to download")
    else:
        print("Error youtube link is invalid")

if __name__ in "__main__":
    main()