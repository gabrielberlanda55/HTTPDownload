from pytube import YouTube,Playlist
#import youtube_dl
import yt_dlp as youtube_dl
import subprocess
import re
import os
import json
import eyed3

TS_YOUTUBE = 1
TS_YOUTUBEMUSIC = 2

class DownloadMusicasYT:
    def __init__(self,link,diretorio,log):
        self.link = link
        self.diretorio = diretorio
        self.dirLog = log
       
    def DownloadYoutube(self):

        def internalDownVideos(File): 
            yt = YouTube(File)
            audio_stream = yt.streams.filter(only_audio=True).first()
            cleaned_title = re.sub(r'[\\/*?:"<>|]', '', yt.title)
            audio_file_path = audio_stream.download(output_path=self.diretorio, filename=cleaned_title + '.webm')

            dirAudioMp3 = audio_file_path[:-5] + '.mp3'
            
            with open(audio_file_path, 'rb') as audio_file:
                subprocess.run(['ffmpeg', '-i', '-', '-b:a', '320k', '-y', dirAudioMp3], stdin=audio_file)

            os.remove(audio_file_path)

            audio_file = eyed3.load(dirAudioMp3)

            if audio_file.tag is None:
                audio_file.initTag()

            audio_file.tag.artist = yt.author
            audio_file.tag.title = yt.title
            audio_file.tag.album = yt.title

            audio_file.tag.save()
        
        if 'playlist?list=' in self.link:

            yt = Playlist(self.link)
            videos = yt.video_urls

            indiceMusica = 0
            qtdMusicas = len(videos)
            for video_url  in videos:
                indiceMusica = indiceMusica + 1
                #self.SalvarLogComunicacao(qtdMusicas=qtdMusicas,BaixandoAtu=indiceMusica,nomeMusicaAtu=YouTube(video_url).title)
                internalDownVideos(video_url)              
        else:
            #self.SalvarLogComunicacao(qtdMusicas=1,BaixandoAtu=1,nomeMusicaAtu=YouTube(self.link).title)
            internalDownVideos(self.link)
        
        #self.SalvarLogComunicacao(finalizou=True)

    def DownloadYoutubeMusic(self):

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            },
        }
        
        # Cria uma instância da classe YoutubeDL
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.link]) 

    def Download(self):
        self.DownloadYoutubeMusic()
        #if 'music.youtube' in self.link:
         #   self.DownloadYoutubeMusic()           
        #else:
        #self.DownloadYoutube()
            
diretorio = ""
link = "https://www.youtube.com/watch?v=CnsJW5KkxcQ"
log = ""
YTDownload = DownloadMusicasYT(diretorio=diretorio,link=link,log=log)
YTDownload.Download()





     
    

    