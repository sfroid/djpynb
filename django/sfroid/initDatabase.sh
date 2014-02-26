sudo supervisorctl stop sfroidsvr
python manage.py dbrestore
sudo supervisorctl start sfroidsvr
