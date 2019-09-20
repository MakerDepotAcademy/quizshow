cd $HOME/Documents/quizshow
git pull -X theirs
pip install -r requirements.txt
cd Display
npm install
cd ..
ln -s $HOME/Documents/quizshow/update.sh update