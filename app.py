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




@app.route('/testemail', methods=['POST', 'GET'])
def testemail():

    sendemail(to_email="tuneman7@hotmai.com",email_subject="test",email_body="test",to_name="tester",attachfiles=[])

    # with app.app_context():
    #     msg = Message(subject="Hello",
    #                     sender=app.config.get("MAIL_USERNAME"),
    #                     recipients=["tuneman7@hotmail.com"], # replace with your email for testing
    #                     body="This is a test email I sent with Gmail and Python!")
    #     mail.send(msg)
    form = sign_up_form(request.form)
    slide_show_width = get_carousel_width()
    return render_template('pages/placeholder.home.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width)




class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_uuid = db.Column(db.String(200),nullable=False)
    email_address = db.Column(db.String(200),nullable=False)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean,nullable=False)
    un_subscribe=db.Column(db.Boolean,nullable=False)
    has_done_donation=db.Column(db.Boolean,nullable=False)
    package_selected=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class user_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    address_1 = db.Column(db.String(200),nullable=False)
    address_2 = db.Column(db.String(200),nullable=True)
    address_3 = db.Column(db.String(200),nullable=True)
    city = db.Column(db.String(200),nullable=False)
    state = db.Column(db.String(200),nullable=False)
    country = db.Column(db.String(200),nullable=False)
    postal_code = db.Column(db.String(200),nullable=False)
    def __repr__(self):
        return '<user_address %r>' % self.id

def user_addresses_all():
    user_list =  user.query.join(user_address,user.id == user_address.user_id)\
        .add_columns(
        user.first_name,
        user.last_name,
        user.email_address,
        user.email_confirmed,
        user.has_done_donation,
        user.package_selected,
        user_address.address_1,
        user_address.address_2,
        user_address.address_3,
        user_address.city,
        user_address.state,
        user_address.country,
        user_address.postal_code
    ).filter(user.id == user_address.user_id).all()
    return user_list

def single_user_address(id_uuid):
    my_user = user.query.join(user_address,user.id == user_address.user_id)\
        .add_columns(
        user.first_name,
        user.last_name,
        user.email_address,
        user.email_confirmed,
        user.has_done_donation,
        user.package_selected,
        user_address.address_1,
        user_address.address_2,
        user_address.address_3,
        user_address.city,
        user_address.state,
        user_address.country,
        user_address.postal_code
    ).filter(user.id == user_address.user_id).filter(user.id_uuid == id_uuid).first()._asdict()
    return my_user

def single_user_address_by_email(email_address):
    my_user = user.query.join(user_address,user.id == user_address.user_id)\
        .add_columns(
        user.first_name,
        user.last_name,
        user.email_address,
        user.email_confirmed,
        user.has_done_donation,
        user.package_selected,
        user_address.address_1,
        user_address.address_2,
        user_address.address_3,
        user_address.city,
        user_address.state,
        user_address.country,
        user_address.postal_code
    ).filter(user.id == user_address.user_id).filter(user.email_address == email_address.lower()).first()
    if my_user is not None:
        return my_user._asdict()
    return my_user



def send_success_notification(email_address):
    user_info = single_user_address_by_email(email_address)
    subject="{}, Thanks For Signing Up".format(user_info["first_name"])
    to_email=email_address
    body="Hi {}, \n\nThanks for signing up for a post card.\n\nWarmly,\n\nDon".format(user_info["first_name"])

    sendemail(to_email=to_email,email_subject=subject,email_body=body,to_name=user_info["first_name"],attachfiles=[])

    subject="{} Just signed up".format(user_info["first_name"])
    to_email='tuneman7@hotmail.com'
    body="A new user just signed up find attached some stuff"

    file_name = email_address +".txt"
    print(user_info)

    # Create an empty string
    my_string = ""
    
    # using for loop only
    for item in user_info:
        if isinstance(user_info[item],str):
            my_string += '"'+ item + '"' + ':' + '"' + user_info[item] + '"' + ' ,'

    str_object = "{" + my_string +"}"
    str_object = str_object.replace(",}","}")
    with open(file_name,"w") as f:
            f.write(json.dumps(json.loads(str_object), indent=4))
        #   f.write(str_object)
    
    cwd = os.getcwd()

    l_files = []
    address_file = cwd + '/' + file_name
    l_files.append(address_file)

    db_file = cwd + '/get_my_post_card.db'
    l_files.append(db_file)

    sendemail(to_email=to_email,email_subject=subject,email_body=body,to_name=user_info["first_name"],attachfiles=l_files)


    os.remove(file_name)

def sendemail(to_email,email_subject,email_body,to_name,attachfiles=[]):
        # read MailerToGo env vars
    mailertogo_host     = "email-smtp.us-west-1.amazonaws.com"
    mailertogo_port     = 587
    mailertogo_user     = "AKIAR7ZOY3QEDBH2UBVZ"
    mailertogo_password = "BExXAEg66L2u8ALKM95oeOy+cxauKd9iuZSwKY+5nly8"
    mailertogo_domain   = "getmypostcard.com"

    # sender
    sender_user = 'Don Irwin'
    sender_email = 'donotreply@getmypostcard.com'
    sender_name = 'Don Irwin'

    # recipient
    recipient_email = to_email # change to recipient email. Make sure to use a real email address in your tests to avoid hard bounces and protect your reputation as a sender.
    recipient_name = to_name

    # subject
    subject = email_subject

    # text body
    body_plain = (email_body)

    # html body
    line_break = '\n' #used to replace line breaks with html breaks
    body_html = f'''<html>
        <head></head>
        <body>
        {'<br/>'.join(email_body.split(line_break))}
        </body>
        </html>'''

    # create message container
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = email.utils.formataddr((recipient_name, recipient_email))

    # prepare plain and html message parts
    part1 = MIMEText(body_plain, 'plain')
    part2 = MIMEText(body_html, 'html')

    # attach parts to message

    message.attach(part1)
    message.attach(part2)

    #now add attachments
    for filename in attachfiles:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
            "Content-Disposition",
            "attachment", filename= filename
            )
            message.attach(part)

    # send the message.
    try:
        server = smtplib.SMTP(mailertogo_host, mailertogo_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mailertogo_user, mailertogo_password)
        print("got this far")
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")

def create_user(email_address,first_name,last_name,address_1,address_2,address_3,city,state,country,postal_code):

    if single_user_address_by_email(email_address) is not None:
        return email_address

    my_user = user()
    my_user.id_uuid = str(uuid.uuid4())
    my_user.first_name = first_name
    my_user.last_name = last_name
    my_user.email_address = email_address.lower()
    my_user.email_confirmed = False
    my_user.un_subscribe = False
    my_user.has_done_donation = False
    my_user.package_selected = 0
    db.session.add(my_user)
    db.session.commit()
    my_address = user_address()
    my_address.user_id = my_user.id;
    my_address.address_1 = address_1
    my_address.address_2 = address_2
    my_address.address_3 = address_3
    my_address.city = city
    my_address.state = state
    my_address.country = country
    my_address.postal_code = postal_code
    db.session.add(my_address)
    db.session.commit()
    send_success_notification(email_address)
    return None


@app.route('/create_csv', methods=['POST', 'GET'])
def create_csv():
    json_files = glob.glob('./data_files/*.txt')

    file_name = "output.csv"
    outlines = []

    for file in json_files:
        with open(file) as json_file:
            my_object = json.load(json_file)
            print(my_object)
            out_line = '\"{}\",'.format(my_object["first_name"].strip() + " " + my_object["last_name"].strip())
            out_line += '\"{}\",'.format(my_object["address_1"].strip() + " " + my_object["address_2"].strip() + " " + my_object["address_3"].strip())
            out_line += '\"{}\",\", {}\",\", {}\",'.format(my_object["city"].strip() , my_object["state"].strip() , my_object["country"].strip())
            outlines.append(out_line+"\n")


    with open(file_name,"w") as f:
        f.writelines(outlines)

    print(file_name)



    
    return file_name



@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    if request.method == 'POST':
        email_address = request.form["email_address"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        address_1 = request.form["address_1"]
        address_2 = request.form["address_2"]
        address_3 = request.form["address_3"]
        city = request.form["city"]
        state = request.form["state"]
        country = request.form["country"]
        postal_code = request.form["postal_code"]
        form = sign_up_form(request.form)
        

        try:
            if not recaptcha.verify():
                return render_template('pages/placeholder.home.html', form=form,already_registered_email = None,is_verified=False)
            my_return = create_user(email_address,first_name,last_name,address_1,address_2,address_3,city,state,country,postal_code) 
            if my_return is not None:
                form = sign_up_form(request.form)
                return render_template('pages/placeholder.home.html', form=form,already_registered_email = my_return,is_verified=None)
            else:
                first_name = request.form["first_name"] 
                slideshow_pictures = glob.glob('./static/images/success_slideshow/*.*')
                slide_show_width = get_carousel_width()
                return render_template('pages/placeholder.success.html', first_name=first_name,slideshow_pictures = slideshow_pictures,slide_show_width=slide_show_width)
        except Exception as e:
            my_dealio = 'There was an issue requesting your postcard.<br/><textbox>{}</textbox>'.format(e)
            return my_dealio

    else:
        return render_template('pages/placeholder.home.html')
        return "bozo"


'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#



@app.route('/')
def home():
    form = sign_up_form(request.form)
    slide_show_width = get_carousel_width()
    return render_template('pages/placeholder.home.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width)


import glob

def get_about_slides_show_images():
    filenames = glob.glob('./images/about_slideshow/*.*')
    return filenames

@app.route('/about')
def about():
    slideshow_pictures = glob.glob('./static/images/about_slideshow/*.*')
    slide_show_width = get_carousel_width()
   # slideshow_pictures = random.shuffle(list(slideshow_pictures))
    return render_template('pages/placeholder.about.html', slideshow_pictures=slideshow_pictures,slide_show_width=slide_show_width)


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


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
