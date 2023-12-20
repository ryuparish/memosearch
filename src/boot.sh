kill -9 $(lsof -t -i:5000)
echo killed pre
python engine/app.py >> backend_log.txt &
cd gui
npm start >> gui_log.txt
kill -9 $(lsof -t -i:5000)
echo killed
