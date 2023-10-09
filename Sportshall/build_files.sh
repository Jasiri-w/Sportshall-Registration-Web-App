echo "Build started at $(date) ~ from Jasiri"
pip install -r requirements.txt

# Make migrations and migrate
python3.9 manage.py migrate

# Check if the superuser already exists
if [ "$(python3.9 manage.py shell -c "import os;from django.contrib.auth.models import User; print(User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists())")" = "False" ]; then
     # Superuser doesn't exist, create one
    echo "Creating superuser..."
    python3.9 manage.py createsuperuser --no-input
else
    # Superuser already exists, skip creation
    echo "Superuser already exists. Skipping creation."
fi

python3.9 manage.py collectstatic --no-input # Flag to force confirmation

echo "Build completed at $(date) ~ Kwaheri"
