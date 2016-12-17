REM Windows only!

REM delete database and migration files
del db.sqlite3
del monosaur\migrations\*
del spend_analyser\migrations\*
del subscriptions\migrations\*

REM regenerate migration files and database based on current models
python manage.py makemigrations monosaur
python manage.py makemigrations spend_analyser
python manage.py makemigrations subscriptions
python manage.py migrate

REM populate database
python manage.py loaddata monosaur\fixtures\category_db.json
python manage.py loaddata monosaur\fixtures\uncategorised_db.json
python manage.py loaddata monosaur\fixtures\company_db.json
python manage.py loaddata subscriptions\fixtures\subscriptions_db.json

REM All done