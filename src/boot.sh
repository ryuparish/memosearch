kill -9 $(lsof -t -i:5000)
echo killed pre
python engine/app.py &
cd gui
npm start
kill -9 $(lsof -t -i:5000)
echo killed
