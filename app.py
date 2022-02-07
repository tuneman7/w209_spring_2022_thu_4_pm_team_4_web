#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import json
import logging
import random
from logging import Formatter, FileHandler
from forms import *
import os
from os import stat_result
from flask import Flask, render_template, url_for, request, redirect, flash,get_flashed_messages ,Markup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Integer
from sqlalchemy.schema import MetaData, Table, Column, ForeignKey
from datetime import datetime
import uuid
import string
from os import environ
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///get_my_post_card.db'


# Dev Recaptcha 127
app.config['RECAPTCHA_SITE_KEY'] = '6LdHDbYdAAAAAGD_3EXjO6pgrwT6-99dGXTKDnsW'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdHDbYdAAAAAGD_3EXjO6pgrwT6-99dGXTKDnsW'
app.config['RECAPTCHA_SECRET_KEY'] = '6LdHDbYdAAAAAHQvFxj10731OQ3eF1UF5b_skayo'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdHDbYdAAAAAHQvFxj10731OQ3eF1UF5b_skayo'
app.config['RECAPTCHA_USE_SSL']= False


# Dev Recaptcha localhost
# app.config['RECAPTCHA_SITE_KEY'] = '6LfJTI0dAAAAAG2P9wOFB2Y0KfyEl0TYpKOsLVam'
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfJTI0dAAAAAG2P9wOFB2Y0KfyEl0TYpKOsLVam'
# app.config['RECAPTCHA_SECRET_KEY'] = '6LfJTI0dAAAAAPpRVYj8M-Co0gKQMK_3yuiME8j9'
# app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfJTI0dAAAAAPpRVYj8M-Co0gKQMK_3yuiME8j9'
# app.config['RECAPTCHA_USE_SSL']= False

#prod Recaptcha www.getmypostcard.com
# app.config['RECAPTCHA_SITE_KEY'] = '6Lf_wpodAAAAAKdAHLjuWNdFyj8xXNNC1r9XQc0g'
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lf_wpodAAAAAKdAHLjuWNdFyj8xXNNC1r9XQc0g'
# app.config['RECAPTCHA_SECRET_KEY'] = '6Lf_wpodAAAAAGGuFaTch1RUaY0St143h2OJhCD2'
# app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lf_wpodAAAAAGGuFaTch1RUaY0St143h2OJhCD2'
# app.config['RECAPTCHA_USE_SSL']= False


#https://get-my-post-card.herokuapp.com/

# app.config['RECAPTCHA_SITE_KEY'] = '6Lc6lLIdAAAAAC5bJVFze_O3XTOOyRm7als_6sSf'
# app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lc6lLIdAAAAAC5bJVFze_O3XTOOyRm7als_6sSf'
# app.config['RECAPTCHA_SECRET_KEY'] = '6Lc6lLIdAAAAAC0iojvCBpSKMjnfaaP5tkHVCYJW'
# app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lc6lLIdAAAAAC0iojvCBpSKMjnfaaP5tkHVCYJW'
# app.config['RECAPTCHA_USE_SSL']= False



from flask_mail import Mail, Message
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'randomchiller@gmail.com',
    "MAIL_PASSWORD": 'Bozo85!$'
}

app.config.update(mail_settings)
mail = Mail(app)


from flask_recaptcha import ReCaptcha

recaptcha = ReCaptcha(app) 


db = SQLAlchemy(app)

import jinja2                                                                                                                                                                                                  
                                                                                                                                                                                     
def include_file(ctx, name):                                                                                                                                                                                   
    env = ctx.environment                                                                                                                                                                                      
    return jinja2.Markup(env.loader.get_source(env, name)[0])
    
def is_local_host():
    url = str(request.url_root)
    if url.__contains__("127.0.0.1"):
        return True
    else:
        return False

def get_carousel_width():
    if is_local_host():
        slide_show_width = 725
    else:
        slide_show_width = 725
    return slide_show_width


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#



@app.route('/')
def home():
    my_output = "test"
    return render_template('pages/placeholder.home.html',my_output)


import glob

def get_about_slides_show_images():
    filenames = glob.glob('./images/about_slideshow/*.*')
    return filenames

@app.route('/about')
def about():
    #slideshow_pictures = glob.glob('./static/images/about_slideshow/*.*')
    #slide_show_width = get_carousel_width()
    #slideshow_pictures = random.shuffle(list(slideshow_pictures))
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    #form = LoginForm(request.form)
    return render_template('forms/login.html')


@app.route('/register')
def register():
    #form = RegisterForm(request.form)
    return render_template('forms/register.html')


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
