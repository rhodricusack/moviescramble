import skvideo.io
import math
import random
import numpy as np

# Scramble video(s) in time - chop into chunks and rearrange
# Rhodri Cusack Trinity College Dublin 2020-10-14, cusackrh@tcd.ie

chunksize=2.0

# Example with just one video
infn=['../videos/moana_saves_turtle.mp4']
outfn='../videos/moana_saves_turtle_scrambled_%fs.mp4'%chunksize

# # Example with two videos intermixed
# infn=['../videos/bathsong.mp4','../videos/mountains.mp4']
# outfn='../videos/mixed_scrambled_%fs.mp4'%chunksize

def load_video(infn):
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
    return metadata,singlevideo,dur,fps
    
# Load up multiple videos in list and shuffle across them
allvideos=None
multi_dur=0
multi_fps=None
for file in infn:
    metadata, singlevideo, dur, fps= load_video(file)
    if allvideos is None:
        allvideos=singlevideo
        multi_fps=fps
    else:
        allvideos=np.concatenate((allvideos,singlevideo),axis=0)
        # if not fps==multi_fps:
        #     raise("FPS must be the same for all videos")
        
    multi_dur+=dur

singlevideo=allvideos
dur=multi_dur
nframes=singlevideo.shape[0]

# Shuffled order
nchunks=math.ceil(dur/chunksize)
rorder=np.random.permutation(nchunks)
inputdict={'-r':fps, '-width':metadata['video']['@width'], '-height':metadata['video']['@height'] }
outputdict={}#{'-r': fps, '-vcodec': 'libx264', '-pix_fmt': 'h264'}
writer=skvideo.io.FFmpegWriter(outfn) #, inputdict=inputdict, outputdict=outputdict)


# Shuffle and output
for chunktime in rorder:
    lowframe=round(chunktime*chunksize*fps)
    highframe=min(nframes, round((chunktime+1)*chunksize*fps))
    for frame in range(lowframe,highframe):
        writer.writeFrame(singlevideo[frame,:,:,:])

