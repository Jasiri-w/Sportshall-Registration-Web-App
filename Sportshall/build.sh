# build_files.sh
pip -r requirements.txt

# make migrations
python manage.py migrate
python manage.py collectstatic