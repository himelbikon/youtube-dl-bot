from moviepy.editor import *
from pytube import YouTube
import os
import shutil


# https://www.youtube.com/watch?v=ktGyuvXWE5s

class TikTokBot:
    def __init__(self):
        self.link = ''
        self.filesize = None
        self.subclips = ['1-5', '6-16']
        self.file_name = 'test_name.mp4'
        self.video_folder = 'videos'
        self.pytube_folder = 'pytube'
        self.invalid_symbles = ['||', '?']

    def save_videos(self, path, subclip):
        self.create_folder(self.video_folder)

        name = f'{path.split("/")[-1][:60]}_{subclip[0]}-{subclip[1]}.mp4'

        clip = VideoFileClip(path).subclip(subclip[0], subclip[1])
        clip.write_videofile(f'{self.video_folder}/{name}')
        clip.close()

        print(f'--> {name} done succeefully!')

    def download_video(self):
        self.delete_folder(self.pytube_folder)
        self.create_folder(self.pytube_folder)
        print('--> Downloading:', self.link)

        video = YouTube(self.link, on_progress_callback=self.downloadCallback)

        video = video.streams.get_highest_resolution()
        self.filesize = video.filesize

        self.create_folder(self.pytube_folder)

        video.download(self.pytube_folder)

        print(f'--> Video downloaded successfully!')

    def downloadCallback(self, chunk, file_handle, bytes_remaining):
        fileSize = self.filesize
        bytes_downloaded = fileSize - bytes_remaining
        percentage = round((bytes_downloaded / fileSize) * 100, 2)
        print(f"{percentage}% Downloaded", end="\r")

    def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def delete_folder(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def min_to_sec(self, minute):
        minute = minute.split('-')

        for i in range(len(minute)):
            if '.' in minute[i]:
                minute[i] = minute[i].split('.')
                minute[i] = str(int(minute[i][0]) * 60 + int(minute[i][1]))

        second = '-'.join(minute)

        return second

    def take_inputs(self):
        self.link = input('Enter video link: ')
        # self.link = 'https://www.youtube.com/watch?v=Q-wgwnref7w'
        self.subclips = list(
            map(self.min_to_sec, input('Enter subclips: ').split()))
        print('--> Subclips:', self.subclips)
        # self.subclips = list(map(self.min_to_sec, ['1.20-1.30', '2.10-2.30', '2.25-2.37']))
        # self.subclips = list(map(self.min_to_sec, ['2-8', '15-20', '30-40']))
        # quit()

    def main(self):
        self.take_inputs()
        self.download_video()

        files = os.listdir(self.pytube_folder)
        for file_path in files:
            if '.mp4' in file_path:
                path = 'pytube/' + file_path

        for symble in self.invalid_symbles:
            if symble in path:
                new_name = path.replace(symble, '')
                os.rename(path, new_name)
                path = new_name

        for clip in self.subclips:
            clip = clip.split('-')
            clip = int(clip[0]), int(clip[1])
            self.save_videos(path, clip)

        shutil.rmtree(self.pytube_folder)

    def start(self):
        print('----------- TikTok Bot by Himel Bikon -----------')

        self.main()


tiktok_bot = TikTokBot()
tiktok_bot.start()
