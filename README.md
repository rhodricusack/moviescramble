# moviescramble
Rhodri Cusack, Trinity College Dublin, 2020-10-14, cusackrh@tcd.ie

## Purpose 
Scrambles movies in time, by cutting into chunks and rearranging. Chunks are 2.0 s by default. It will scramble more than movie, intermixing the chunks, if you give it a list of filenames in inpth

## Installation
To set up conda environment use
conda create --name moviescramble --file requirements.txt

You also need ffmpeg and ffprobe, on Ubuntu 18.04 

sudo snap install ffmpeg

(which I think should also install ffprobe, but check and correct this README if necessary!)


