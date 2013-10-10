#! /usr/bin/env bash

# the two repo of files
#PATH_A="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/MA_CLEM_1"
#PATH_B="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/MA_ALEX_1"
PATH_A="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/BOUCHE_CLEM"
PATH_B="/home/aleray/work/osp.work.maisons-phenix.www/tools/compositions_automatiques/MARQUEURS/BOUCHE_CLEM"

# The number of files to pick
N=5

# The file that will record our composition
FILELIST='/tmp/list.txt'

# We empty that file first
echo > $FILELIST

#find "${PATH_A}" -iname "*.aiff" -printf "'%p'\n" | shuf -n $N

# Our collections of files
ARRAY_A=(`find "${PATH_A}" -iname "*.aiff" -printf "file@'%p'\n" | shuf -n $N | tr "\n" " "`)
ARRAY_B=(`find "${PATH_B}" -iname "*.aiff" -printf "file@'%p'\n" | shuf -n $N | tr "\n" " "`)

for i in {0..4}
do
   echo ${ARRAY_A[$i]} | tr "@" " " >> "$FILELIST"
   echo ${ARRAY_B[$i]} | tr "@" " " >> "$FILELIST"
done

ffmpeg -y -f concat -i "$FILELIST" -c copy /tmp/output.aiff
mplayer /tmp/output.aiff
