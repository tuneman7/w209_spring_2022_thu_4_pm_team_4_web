#!/bin/bash
rm *.db
python create_db.py
#python app.py
gunicorn --bind 0.0.0.0:5000 app:app --threads 20