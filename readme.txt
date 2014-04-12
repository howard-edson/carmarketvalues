pip installs of apps
Django==1.6
Pillow==2.4.0
South==0.8.4
django-bootstrap3==4.2.0
django-crispy-forms==1.4.0
feedparser==5.1.3
psycopg2==2.5.2
wsgiref==0.1.2
docutils==0.11

pull into your local branch; currently registration does not work
it will be implemented in next section

syncdb
then
./manage.py schemamigration cmv_app --initial 

I have a script (populate.py) made to populate random saved searches for three different users.

if we click a Saved Search for User, it should relevant postings but currently it does not

That will be implemented soon
