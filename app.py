#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify,escape
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

from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.altair_renderings import AltairRenderings
import altair as alt


@app.route('/fourchartmatrix', methods=['POST', 'GET'])
def fourchartmatrix():
    my_altair = AltairRenderings()

    source_country = "United States"
    target_country = "China"
    if request.method == 'POST':
        source_country = request.form["source_country"]
        target_country = request.form["target_country"]
        
    line_chart_1 = my_altair.get_altaire_line_chart_county_trade_for_matrix(source_country, target_country)
    top5_partners = my_altair.get_altaire_bar_top5_partners_for_matrix(source_country)
    top_5_products = my_altair.get_altaire_dual_axis_bar_top5(source_country)
    
    form = CountryDetailVisualizationForm(request.form,current_target_country=target_country,current_source_country=source_country) 
    return render_template('pages/placeholder.home.html',country_list=None,visualization_form=None,chart_json = chart_json,form=form,current_source_country=source_country,current_target_country=target_country)


@app.route('/', methods=['POST', 'GET'])
def home():

    my_altair = AltairRenderings()
    junk_json,map_json = my_altair.get_world_map()
    country_list = my_altair.get_top_20_countries()
    return render_template('pages/placeholder.home.html',
    map_json=map_json.to_json(),
    country_list=json.dumps(country_list))

    

@app.route('/top5trading', methods=['POST', 'GET'])
def top5trading():
    my_altair = AltairRenderings()

    source_country = "United States"
    if request.method == 'POST':
        source_country = request.form["source_country"]
        
    chart_json = my_altair.get_altaire_bar_top5_partners(source_country).to_json()
    form = CountryToWorldVisualizationForm(request.form,current_source_country=source_country) 
    return render_template('pages/placeholder.top5trading.html',country_list=None,visualization_form=None,chart_json = chart_json,form=form,current_source_country=source_country)


@app.route('/top5products', methods=['POST', 'GET'])
def top5products():
    my_altair = AltairRenderings()

    source_country = "United States"
    if request.method == 'POST':
        source_country = request.form["source_country"]
        
    chart_json = my_altair.get_altaire_dual_axis_bar_top5(source_country).to_json()
    form = CountryToWorldVisualizationForm(request.form,current_source_country=source_country) 
    return render_template('pages/placeholder.top5trading.html',country_list=None,visualization_form=None,chart_json = chart_json,form=form,current_source_country=source_country)

@app.route('/piechart', methods=['POST', 'GET'])
#def pie_chart():
#    my_altair = AltairRenderings()

#    source_country = "United States"
#    target_country = "China"
#    direction = "exports"
#    if request.method == 'POST':
#        source_country = request.form["source_country"]
#        target_country = request.form["target_country"]
#        direction = request.form["exports"]

#    chart_json = my_altair.get_altaire_dual_pie_chart_by_types(source_country, target_country, direction).to_json()
#    form = CountryVisualizationFormWithDirection(request.form,current_target_country=target_country,current_source_country=source_country, direction = direction) 
#    return render_template('pages/placeholder.piechart.html',country_list=None,visualization_form=None,chart_json = chart_json,form=form,current_source_country=source_country,current_target_country=target_country, direction = direction)
def China_pie_chart():
    my_altair = AltairRenderings()

    source_country = "China"
    chart_json = my_altair.get_altaire_multi_charts_for_China().to_json()
    return render_template('pages/placeholder.piechart.html',country_list=None,visualization_form=None,form = None, chart_json = chart_json)


@app.route('/world1')
def world1():
    my_altair = AltairRenderings()
    junk_json,map_json = my_altair.get_world_map()
    return render_template('pages/placeholder.world.html',chart_json=map_json.to_json())

@app.route('/worldmodal')
def worldmodal():
    my_altair = AltairRenderings()
    junk_json,map_json = my_altair.get_world_map()
    country_list = my_altair.get_top_20_countries()
    return render_template('pages/placeholder.world_modal.html',map_json=map_json.to_json(),country_list=json.dumps(country_list))


@app.route('/world')
def world():
    my_altair = AltairRenderings()
    map_json,junk_map_json = my_altair.get_world_map()
    return render_template('pages/placeholder.world.html',chart_json=map_json)

@app.route('/mynewmap')
def my_new_map():
    my_altair = AltairRenderings()
    my_map = my_altair.my_new_map()
    return render_template('pages/placeholder.world.html',chart_json=my_map.to_json())



@app.route("/world_trade_region",methods=["POST","GET"])
def world_trade_region():
    print("mybozo")
    return jsonify({'htmlresponse': render_template('pages/placeholder.world_events.html')})

@app.route("/covid_impact_content",methods=["POST","GET"])
def covid_impact_content():
    print("mybozo")
    return jsonify({'htmlresponse': render_template('pages/placeholder.covid_impact.html')})


@app.route("/nafta_trade_content",methods=["POST","GET"])
def nafta_trade_content():
    print("mybozo")
    return jsonify({'htmlresponse': render_template('pages/placeholder.nafta_trade.html')})

@app.route("/china_trade_content",methods=["POST","GET"])
def china_trade_content():
    print("mybozo china_trade_content")
    #placeholder.china_trade.html
    return jsonify({'htmlresponse': render_template('pages/placeholder.nafta_trade.html')})
    


@app.route("/mapmodaldata",methods=["POST","GET"])
def ajaxfile():

    my_altair = AltairRenderings()

    title = ""
    source_country = "United States"
    target_country = "World"
    if request.method == 'POST':
        source_country = request.form["source_country"]
        target_country = request.form["target_country"]
    if target_country.lower() == "world":        
        title = "Trade between <b>" + source_country + "</b> and <b>" + target_country + "</b> top 20 trading nations. To see trade with another country select from drop-down: "
        chart_json = my_altair.get_charts_for_click_from_world_map(source_country,width=350,height=200).to_json()
        form = CountryToWorldVisualizationFormWithWorld(request.form,current_source_country=source_country) 
        return jsonify({'htmlresponse': render_template('modal/modal_chart.html',visualization_form=None,chart_json = chart_json,form=form,source_country=source_country,current_target_country=target_country,country_list=None,modal_title=escape(title))})

    if target_country.lower() !="world":
        title = "Trade between <b>" + source_country + "</b> and <b>" + target_country + "</b>. To see <b>" + source_country +"'s trade with another country select from drop-down: "
        chart_json = my_altair.get_charts_for_country_dill_down(source_country,target_country,width=350,height=200).to_json()
        form = CountryToWorldVisualizationFormWithWorld(request.form,current_source_country=source_country) 
        return jsonify({'htmlresponse': render_template('modal/modal_chart_source_target.html',visualization_form=None,chart_json = chart_json,form=form,source_country=source_country,target_country=target_country,country_list=None,modal_title=escape(title))})

        #"modal_chart_source_target.html"
 


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
