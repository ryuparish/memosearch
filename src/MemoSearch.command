#!/bin/bash
lsof -t -i tcp:5000 | xargs kill && lsof -t -i tcp:4444 | xargs kill && lsof -t -i tcp:3000 | xargs kill &
export FLASK_APP=~/Code/memosearch/src/backend/src/memosearch/ && flask run &
npm start --prefix ~/Code/memosearch/src/frontend/ &
