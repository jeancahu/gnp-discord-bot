#!/bin/bash

while :
do
    clear
    python bot.py &

    inotifywait -e close_write bot.py

    if [[ "$(jobs)" ]]
    then
        kill -s 15 %%
    fi
done

exit 0
