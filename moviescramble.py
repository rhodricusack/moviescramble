import skvideo.io
import math
import random
import numpy as np

# Scramble video(s) in time - chop into chunks and rearrange
# Rhodri Cusack Trinity College Dublin 2020-10-14, cusackrh@tcd.ie

# 2020-10-19, v0.1: 
#    Chop off last partial chunk, so that all chunks in a randomisation are of the chunksize
#    Implement alternate and random mixstyles 

# Length of randomisation chunk
chunksize=8.0
# If movies have different heights, can clip centre of them to height specified here. Otherwise put None
clipheight=266
# When multiple movies, can choose how they are mixed - alternate clips from each movie or completely random
mixstyle='alternate' # alternate | random


# Example with just one video
# infn=['../videos/moana_saves_turtle.mp4']
# outfn='../videos/moana_saves_turtle_scrambled_%fs.mp4'%chunksize

# infn=['../videos/bighero6.mp4']
# outfn='../videos/bighero6_scrambled_%fs.mp4'%chunksize

# Example with two videos intermixed
infn=['../videos/moana_saves_turtle.mp4','../videos/bighero6.mp4']
outfn='../videos/moana_bighero_scrambled_%fs_%s.mp4'%(chunksize, mixstyle)



# # Example with two videos intermixed
# infn=['../videos/bathsong.mp4','../videos/mountains.mp4']
# outfn='../videos/mixed_scrambled_%fs.mp4'%chunksize

def load_video(infn, clipheight=None):
    # Load metadata
    metadata = skvideo.io.ffprobe(infn)
    dur=float(metadata['video']['@duration'])       
    nframes=int(float(metadata['video']['@nb_frames']))
    fps=nframes/dur
    print('Video %s duration %f nrames %d fps %f'%(infn,dur,nframes,fps))

    # Load a video
    singlevideo=skvideo.io.vread(infn)
    print(singlevideo.shape)
    singlevideo=singlevideo.astype(np.uint8)

    # Clip height?
    if clipheight:
        h=singlevideo.shape[1]
        singlevideo=singlevideo[:,round(h/2-clipheight/2):round(h/2+clipheight/2),:,:]
        metadata['video']['@height']=clipheight
        print('Clipped height to %s'%clipheight)
    return metadata,singlevideo,dur,fps
    
# Load up multiple videos in list and shuffle across them
allvideos=[]
alldur=[]
total_dur=0 # total of all movies
multi_fps=None
for file in infn:
    metadata, singlevideo, dur, fps= load_video(file, clipheight)
    alldur.append(dur)
    allvideos.append(singlevideo)
    total_dur+=dur
nmovies=len(infn)

# Get random order for each movie
#  Now insist on chunks being whole chunks (drop last partial chunk)
allnchunks=[math.floor(x/chunksize) for x in alldur]
allrorder=[np.random.permutation(x) for x in allnchunks]

# In mixtures, equal number of chunks from each movie
minnchunks=np.min(allnchunks)

# Order of movies
movieorder=list(np.arange(nmovies)) * minnchunks
if mixstyle=='random':
    movieorder=np.random.shuffle(movieorder)
elif mixstyle=='alternate':
    pass
else:
    raise('Unknown mixstyle %s'%mixstyle)

# Ready to write
writer=skvideo.io.FFmpegWriter(outfn) 

# Shuffle and output
allchunkcount=[0]*nmovies
for chunkmovie in movieorder:
    chunktime=allrorder[chunkmovie][allchunkcount[chunkmovie]]
    allchunkcount[chunkmovie]+=1
    lowframe=round(chunktime*chunksize*fps)
    highframe=round((chunktime+1)*chunksize*fps)
    for frame in range(lowframe,highframe):
        writer.writeFrame(allvideos[chunkmovie][frame,:,:,:])

