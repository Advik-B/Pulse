import pytube
import os
import py7zr
import typing

FS_NAME = 'FileStorage'

def search_(query:str, max_results: int=10) -> list[pytube.YouTube]:
    yt = pytube.Search(query)
    results = []
    current_inc = 0
    for result in yt.results:
        if current_inc >= max_results:
            break
        if result.vid_info['videoDetails'].get('isLive') is None:
            results.append(result)
            current_inc += 1
    
    return results

def download_audio(video: pytube.YouTube, cwd: str=os.path.abspath(FS_NAME)):
    stream: pytube.Stream = video.streams.filter(only_audio=True).first()
    with open(os.path.join(cwd, f'{video.video_id}.mp3'), 'wb') as f:
        stream.stream_to_buffer(f)
    # Compress the file
    os.chdir(cwd)
    with py7zr.SevenZipFile(f'{video.video_id}.mp3.7z', 'w') as z:
        z.write(f'{video.video_id}.mp3')
    os.chdir("..")
    return os.path.abspath(f'{os.path.join(FS_NAME, video.video_id)}.mp3')

def getinfo(video: str):
    return pytube.YouTube(video)

def get_playlist(url: str) -> list:
    yt = pytube.Playlist(url)
    return list(yt.videos)

def index_for_video_locally(
    video: typing.Union[pytube.YouTube, str],
    cwd: str=os.path.join(
        os.getcwd(),
        'FileStorage'
    )
    ):
    if type(video) is str:
        video = pytube.YouTube(video)
    v_id = video.video_id
    for f in os.listdir(cwd):
        if v_id == f.removesuffix('.mp3.7z'):
            return os.path.join(cwd, f)

def unzip(file: str) -> str:
    os.chdir(FS_NAME)
    with py7zr.SevenZipFile(file.__add__('.mp3.7z'), 'r') as z:
        z.extractall('.')

    os.chdir("..")
    return os.path.join(FS_NAME, f'{file}.mp3')