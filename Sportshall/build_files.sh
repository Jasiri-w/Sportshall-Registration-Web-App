# build_files.sh
echo "Build started at $(date) ~ from Jasiri"
pip install -r requirements.txt

# make migrations
python manage.py migrate
python manage.py collectstatic

echo "Build completed at $(date) ~ Kwaheri"