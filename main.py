from __future__ import unicode_literals
import youtube_dl
from os import listdir
from os.path import isfile, isdir, join
import os
import re
import webvtt
from moviepy.editor import *
from yattag import Doc
class myLogger(object):
    def debug(self, msg):
       pass
    def warning(self,msg):
        pass
    def error(self,msg):
        print(msg)
def my_hook(d):
    if(d['status'] == 'finished'):
        print("Finished : ", d['filename'])
        return


ydl_opts = {
    'format': 'best',
    'logger': myLogger(),
    'writeautomaticsub': True,
    'allsubtitles': True,
    'progress_hooks': [my_hook],
    'subtitlesformat': "srt",
    'outtmpl': "./DD_%(playlist_index)s - %(title)s/%(title)s.mp4",
}

sub = ["zh-Hant"]


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([sys.argv[-1]])
mypath = '.'
thisDir = listdir(mypath)
for fileOrDir in thisDir:
    fullpath = join(mypath,fileOrDir)
    if isdir(fullpath) and (re.search("DD_*", fileOrDir)):
        print(fullpath)
        videopath = ""
        subpath = []
        insideDir = listdir(fullpath)
        for srtandvideo in insideDir:
            insideDirFileFullPath = join(fullpath,srtandvideo)
            if isfile(insideDirFileFullPath) and (re.search(".mp4", srtandvideo)):
                videopath = insideDirFileFullPath
            else:
                for i in sub:
                    if isfile(insideDirFileFullPath) and (re.search("."+i+".vtt", srtandvideo)):
                        subpath.append(insideDirFileFullPath)
        #
        #print("video",videopath)
        #print("subpath", subpath)
        savepath = join(mypath, "out"+fileOrDir)
        try:
            os.mkdir(savepath)
        except Exception as e:
            print(e)

        try:
            video = VideoFileClip(videopath)
            doc, tag, text = Doc().tagtext()
            with tag('html'):
                with tag('body'):
                    with tag('h1'):
                        text(fileOrDir)
                i = 0
                for subP in subpath:
                    with tag('h2'):
                        text(subP)

                    for caption in webvtt.read(subP):
                        with tag('h3'):
                            text(caption.text)

                        try:
                            # print(caption.start, caption.end, caption.text)
                            video.subclip(caption.start, caption.end).write_gif(join(savepath, str(i) + ".gif"), fps=15)
                            with tag('div'):
                                doc.stag('img', src=str(i) + ".gif", alt=caption.start)
                        except Exception as e:
                            print(e)

                        i += 1
            html = open(join(savepath, "index.html"), 'w')
            html.write(doc.getvalue())
            html.close()
        except Exception as e:
            print(e)

