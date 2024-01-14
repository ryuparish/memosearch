#!/bin/bash
lsof -t -i tcp:5000 | xargs kill && lsof -t -i tcp:4444 | xargs kill && lsof -t -i tcp:3000 | xargs kill &
flask --app memosearch run &
npm start --prefix ./frontend/ &
