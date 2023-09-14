#!/bin/bash
rm *.db
python create_db.py
python app.py

