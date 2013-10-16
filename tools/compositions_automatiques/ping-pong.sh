#! /usr/bin/env bash

# the two repo of files
#PATH_A="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/MA_CLEM_1"
#PATH_B="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/MA_ALEX_1"
#PATH_A="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/BOUCHE_CLEM"
#PATH_B="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/BOUCHE_CLEM"

PATH_A="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/ALEX"
#PATH_B="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/NEW_INDEX_CLEMENT_RESTER_PARTIR"
PATH_B="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/INDEX_M"

# The number of files to pick
N=5

# The file that will record our composition
FILELIST='/tmp/list.txt'

# We empty that file first
> $FILELIST

ffmpeg -ar 44100 -t 1 -f s16le -acodec pcm_s16le -ac 2 -i /dev/zero -acodec copy /tmp/silence.aiff

#find "${PATH_A}" -iname "*.aiff" -printf "'%p'\n" | shuf -n $N

# Our collections of files
ARRAY_A=(`find "${PATH_A}" -iname "*.aiff" -printf "file@'%p'\n" | shuf -n $N | tr "\n" " "`)
ARRAY_B=(`find "${PATH_B}" -iname "*.aiff" -printf "file@'%p'\n" | shuf -n $N | tr "\n" " "`)

for i in {0..4}
do
   echo ${ARRAY_A[$i]} | tr "@" " " >> "$FILELIST"
   echo "file '/tmp/silence.aiff'" >> "$FILELIST"
   echo ${ARRAY_B[$i]} | tr "@" " " >> "$FILELIST"
   echo "file '/tmp/silence.aiff'" >> "$FILELIST"
done

ffmpeg -y -f concat -i "$FILELIST" -c copy /tmp/output.aiff
mplayer /tmp/output.aiff
