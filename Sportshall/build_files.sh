# build_files.sh
echo "Build started at $(date) ~ from Jasiri"
pip install -r requirements.txt

# make migrations
python3.9 manage.py migrate
python3.9 manage.py collectstatic --no-input # Flag to force confirmation

echo "Build completed at $(date) ~ Kwaheri"