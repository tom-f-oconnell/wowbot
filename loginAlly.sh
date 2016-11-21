#!/bin/bash

wine /media/tb/Games/wow-4.3.4/wow_434.exe 1>/dev/null 2>/dev/null &
sleep 1
wine /media/tb/Games/wow-4.3.4/wow_434.exe 1>/dev/null 2>/dev/null &
sleep 1
wine /media/tb/Games/wow-4.3.4/wow_434.exe 1>/dev/null 2>/dev/null &
sleep 1
wine /media/tb/Games/wow-4.3.4/wow_434.exe 1>/dev/null 2>/dev/null &
sleep 1
wine /media/tb/Games/wow-4.3.4/wow_434.exe 1>/dev/null 2>/dev/null &

sleep 11

IDS=()
regex="0x........"

width=600
height=350
curr_h=300
curr_w=0
i=0

for id in $(wmctrl -l | grep "0x........\ \ 0\ blackbox\ Wor"); do 
    if [[ $id =~ $regex ]]; then
        IDS+=($id)
        echo $curr_w
        echo $curr_h
        echo $width
        echo $height
        wmctrl -i -r $id -e 0,$curr_w,$curr_h,$width,$height
        curr_w=$(($curr_w + $width + 20))
        if [ $i -eq 2 ]; then
            curr_h=$(($curr_h + $height + 20))
            curr_w=0
        fi
        i=$(($i + 1))
        sleep 2
    fi
done

USERS=("zgmigae" "zhmqxtg" "zmpzskks" "zoxfyuyss" "zsdosuys")
PASSWS=("49MmVvmAkG" "9dnVvYG4C6" "trr7rKRVZh" "jSsx6HKMtd" "QJZJxtRaw4")

for ((i=0; i<${#IDS[@]}; ++i)); do
    echo ${IDS[i]}
    echo ${USERS[i]}
    echo ${PASSWS[i]}
    wmctrl -i -a ${IDS[i]}
    sleep 0.1
    xvkbd -text "${USERS[i]}\t${PASSWS[i]}\r" -delay 80
    sleep 0.1
done

sleep 1

for ((i=0; i<${#IDS[@]}; ++i)); do
    echo ${IDS[i]}
    wmctrl -i -a ${IDS[i]}
    sleep 0.1
    xvkbd -text "\r"
    sleep 0.2
done

