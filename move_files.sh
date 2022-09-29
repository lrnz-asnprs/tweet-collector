#!/bin/bash
for i in $(pwd)/*[0-9].json
    do
        mv "$i" $(pwd)/data/fakenews_tw_output
done
