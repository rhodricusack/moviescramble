import skvideo.io
import math
import random
import numpy as np

chunksize=2.0
infn=['moana_saves_turtle.mp4']
outfn='moana_saves_turtle_%fs.mp4'%chunksize

def load_video(infn):
    # Load metadata
    metadata = skvideo.io.ffprobe(infn)
    dur=float(metadata['video']['@duration'])       
    nframes=int(float(metadata['video']['@nb_frames']))
    fps=nframes/dur
    print('Video %s duration %f nrames %d fps %f'%(infn,dur,nframes,fps))

    # Load all video
    allvideo=skvideo.io.vread(infn)
    print(allvideo.shape)
    allvideo=allvideo.astype(np.uint8)
    return metadata,allvideo,dur,fps
    
# Load up multiple videos in list and shuffle across them
multi_allvideo=None
multi_dur=0
multi_fps=None
for file in infn:
    metadata, allvideo, dur, fps= load_video(file)
    if multi_allvideo is None:
        multi_allvideo=allvideo
        multi_fps=fps
    else:
        multi_allvideo=np.concatenate((multi_allvideo,allvideo),axis=0)
        # if not fps==multi_fps:
        #     raise("FPS must be the same for all videos")
        
    multi_dur+=dur

allvideo=multi_allvideo
dur=multi_dur
nframes=allvideo.shape[0]

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
        writer.writeFrame(allvideo[frame,:,:,:])


# for frame in reader.nextFrame():
#     nframe+=1
#     skvideo.io.vwrite(outfn, frame)
#     if nframe % 100 ==0:
#         print(f'Frame {nframe}')
