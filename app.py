#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify,escape,make_response
# from flask.ext.sqlalchemy import SQLAlchemy
import json
import logging
import random
from logging import Formatter, FileHandler
from forms import *
import os, time
from os import stat_result
from flask import Flask, render_template, url_for, request, redirect, flash,get_flashed_messages ,Markup
from flask_mail import Mail, Message
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
from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.altair_renderings import AltairRenderings
from libraries.utility import Utility
import altair as alt
from datetime import timedelta

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///get_my_post_card.db'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "mids.2022.spr.w209.th.4.tm.4@gmail.com",
    "MAIL_PASSWORD": "Spring2022!$"
}

app.config.update(mail_settings)
mail = Mail(app)


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

import glob

@app.route('/clearthisuser', methods=['POST', 'GET'])
def clear_this_user():
    res = make_response("clear cookies")
    expire_date = datetime.now()
    expire_date = expire_date + timedelta(minutes=-10)
    res.delete_cookie('sessionID')
    return res

def check_if_new_user():
    for key in request.cookies.keys():
        print("key=",key)
        if key=='sessionID':
            print("FOUND THE DEALIO")
            return False

    return True




# def check_if_new_user():
#     my_util = Utility()
#     filenames = glob.glob('./ip_tracking_directory/*.ip')
    
#     file_dict = {}

#     ip_file_name = request.remote_addr + ".ip"

#     in_directory = False

#     for f in filenames:
#         age = time.time() - os.path.getmtime(f)
#         minutes = int(age) / 60
#         if minutes > 10:
#             os.remove(f)
#             continue
#         if ip_file_name in f:
#             in_directory = True
#             str_file_name = os.path.join(my_util.get_this_dir(),"ip_tracking_directory",ip_file_name)
#             my_util.write_data_to_file(str_file_name=str_file_name,content_to_write="")

            
    
#     if in_directory == False:
#         str_file_name = os.path.join(my_util.get_this_dir(),"ip_tracking_directory",ip_file_name)
#         my_util.write_data_to_file(str_file_name=str_file_name,content_to_write="")

#     if in_directory == False:
#         return True
#     else:
#         return False


@app.route('/send_email', methods=['POST', 'GET'])
def send_email():

    form = email_form()
    success = False
    slide_show_width = get_carousel_width()    
    if request.method == 'POST':
        form = email_form(request.form)
        if not form.validate():
            print("bozo")
            return jsonify({'htmlresponse': render_template('modal/email_modal.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width,success=success)})
        else:
            print("valid")
            first_name = request.form["first_name"] 
            email_address = request.form["email_address"]
            message_text = request.form["message_text"]
            line_break = '\n'  # used to replace line breaks with html breaks

            email_body = "Email from W209 Project "+ datetime.now().strftime("%d-%b-%Y-%H:%M:%S") + "\n" \
                         "Sender's Name: " + first_name + "\n" \
                         "Sender's Email: " + email_address + "\n\n" \
                         "Sender's Message: \n\n" + message_text + "\n\n" \

            with app.app_context():
                msg = Message(subject="Email From MIDS W209 Project Spring 2022 "+ datetime.now().strftime("%d-%b-%Y-%H:%M:%S"),
                              sender=app.config.get("MAIL_USERNAME"),
                              recipients="sy7chen@ischool.berkeley.edu,don.irwin@ischool.berkeley.edu,justin.peabody@ischool.berkeley.edu,zhangs@ischool.berkeley.edu".split(","),  # replace with your email for testing
                              body=email_body)
                mail.send(msg)
                success=True

            return jsonify({'htmlresponse': render_template('modal/email_modal.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width,success=success)})
    else:
        return jsonify({'htmlresponse': render_template('modal/email_modal.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width,success=success)})


        



    #return render_template('pages/placeholder.home.html',form=form,already_registered_email=None,is_verified=None,slide_show_width=slide_show_width)
    

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
    is_new_user = check_if_new_user()

    print("is_new_user=",is_new_user)

    junk_json,map_json = my_altair.get_world_map()
    country_list = my_altair.get_top_20_countries()

    res = make_response(render_template('pages/placeholder.home.html',
            map_json=map_json.to_json(),
            country_list=json.dumps(country_list),
            is_new_user = is_new_user ))
    expire_date = datetime.now()
    expire_date = expire_date + timedelta(minutes=10)
    print("expire_date=",expire_date)
    print("request.base_url=",request.base_url)
    res.set_cookie('sessionID', 'fido',max_age=60*10)
    return res



    

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

    # source_country = "China"
    # chart_json = my_altair.get_altaire_multi_charts_for_China().to_json()
    # return render_template('pages/placeholder.piechart.html',country_list=None,visualization_form=None,form = None, chart_json = chart_json)

#def Covid_chart():
#    my_altair = AltairRenderings()

    chart_json = my_altair.get_altaire_yoy_trade_per_GDP_for_matrix('United States', 'Canada').to_json()
    return render_template('pages/placeholder.piechart.html',country_list=None,visualization_form=None,form = None, chart_json = chart_json)

@app.route('/china')
def china():
    my_altair = AltairRenderings()

    chart_json = my_altair.get_china_section_1().to_json()
    return render_template('pages/placeholder.piechart.html',country_list=None,visualization_form=None,form = None, chart_json = chart_json)

@app.route('/china1')
def china1():
    my_altair = AltairRenderings()

    chart_json = my_altair.get_china_section_2().to_json()
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
    my_data = Import_Export_Data()
    world_events = my_data.get_world_event_data();
    return jsonify({'htmlresponse': render_template('pages/section_content/placeholder.world_events.html',world_events=world_events)})

@app.route("/covid_impact_content",methods=["POST","GET"])
def covid_impact_content():
    print("mybozo")
    return jsonify({'htmlresponse': render_template('pages/section_content/placeholder.covid_impact.html')})


@app.route("/nafta_trade_content",methods=["POST","GET"])
def nafta_trade_content():
    print("mybozo")
    return jsonify({'htmlresponse': render_template('pages/section_content/placeholder.nafta_trade.html')})

@app.route("/china_trade_content",methods=["POST","GET"])
def china_trade_content():
    print("mybozo china_trade_content")
    #placeholder.china_trade.html
    return jsonify({'htmlresponse': render_template('pages/section_content/placeholder.china_trade.html')})

@app.route("/introduction_content",methods=["POST","GET"])
def introduction_content():
    print("mybozo introduction_content")
    #placeholder.china_trade.html
    return jsonify({'htmlresponse': render_template('pages/section_content/placeholder.introduction.html')})

@app.route("/eu_trade_content",methods=["POST","GET"])
def eu_trade_content():
    print("mybozo eu_trade_content")
    #placeholder.china_trade.html
    return jsonify({'htmlresponse': render_template('pages/section_content/placeholder.eu_trade.html')})



@app.route("/render_world_event_graphs",methods=["POST","GET"])
def render_world_event_graphs():
    my_altair = AltairRenderings()
    utility = Utility()
    print("render_world_event_graphs()")
    event_name = "JCPOA"
    is_json_graph = True
    chart_json=None
    event_text=None
    slide_no = None
    image_path = None
    event_hyperlink = None
    flip_animation = False
    if request.method == 'POST':
        event_name = request.form["event_name"]
        slide_no = request.form["slide_no"]


    try:
        file_name = event_name.lower() +"_"+ slide_no+".txt"
        load_file_name = os.path.join(utility.get_this_dir(),"data","world_events",file_name)
        print(load_file_name)
        event_text = utility.get_data_from_file(load_file_name)
    except:
        fido="dido"


    if event_name == "RCEP":
        if slide_no == "1":
            chart_json = my_altair.get_asian_trading_partners().to_json()
        if slide_no == "2":
            chart_json = my_altair.get_lines_for_top5_countries().to_json()
        file_name = event_name.lower() +"_"+ slide_no+".txt"
        load_file_name = os.path.join(utility.get_this_dir(),"data","world_events",file_name)
        event_text = utility.get_data_from_file(load_file_name)

    #am here
    if event_name == "JCPOA":
        if slide_no == "1":
            chart_json = my_altair.get_altaire_line_chart_county_trade_for_matrix("Iran","World",width=600,height=300).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).to_json()
        if slide_no == "2":
            chart_json = my_altair.get_iran_trade_deal_line_charts().to_json()
        if slide_no == "3":
            chart_json = my_altair.get_third_page_jcpoa_charts().to_json()
        if slide_no == "4":
            chart_json = my_altair.get_fourt_page_of_jcpoa_chart().to_json()

    if event_name == "USChinatradeWar":
        if slide_no == "1":
            print("mybozo")
            chart_json = my_altair.get_china_trade_with_us_pie_chart(width=150,height=150).to_json()
        if slide_no == "2":
            print("mybozo")
            chart_json = my_altair.get_altaire_line_chart_county_trade_for_matrix("United States","China",width=600,height=300).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).to_json()
        if slide_no == "3":
            print("mybozo")
            chart_json = my_altair.china_trade_war_slide_three().configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).to_json()                

        if slide_no == "4":
            print("mybozo")
            chart_json = my_altair.get_altaire_dual_pie_chart_by_types_for_matrix("United States",
            "China",
            "exports",width=600,height=300).to_json()


        if slide_no == "5":
            print("mybozo")
            chart_json = my_altair.china_trade_war_slide_four().configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).to_json()            

        if slide_no == "6":
            print("mybozo")
            chart_json = my_altair.china_trade_war_slide_five().configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).to_json()            

        if slide_no == "7":
            print("event no=",slide_no)
            is_json_graph = False
            chart_json = None
            event_hyperlink = "https://www.wired.com/story/biden-china-policy-looks-like-trumps/"
            image_path = "./static/images/nothing_has_changed.jpg"
            print(event_hyperlink)


        if slide_no == "8":
            print("event no=",slide_no)
            is_json_graph = False
            chart_json = None
            event_hyperlink = "https://www.bloomberg.com/graphics/2022-china-nationalistic-online-shoppers/?srnd=bigtake&utm_medium=cpc_social&utm_source=facebook&utm_campaign=BLOM_ENG_EDITORL_COUSA_FB_SO_WENG_FOCUSPROSX_INTST_00XXXXCPM_2PFB_XXXX_GENERALINTSTX_XXXXX_COUSA_XXXXX_ALLFOA_CHID_C5_EN_PG_NFLINKS&dclid=CLv9icPXtfYCFYyJZAodquwDZQ"
            image_path = "./static/images/lede.gif"
            flip_animation = True
            print(event_hyperlink)


    if event_name.lower() == "covid19":
        print("mybozo=",event_name.lower())
        if slide_no == "1":
            chart_json = my_altair.get_altaire_scatter_Covid().configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).to_json()



    return jsonify({'htmlresponse': render_template('modal/modal_world_event.html',
    event_name=event_name,
    chart_json=chart_json,
    event_text=event_text,
    event_hyperlink=event_hyperlink,
    image_path=image_path,
    flip_animation=flip_animation)})





@app.route("/render_china_graphs",methods=["POST","GET"])
def render_china_graphs():
    my_altair = AltairRenderings()
    utility = Utility()
    print("render_china_graphs()")
    event_name = "JCPOA"
    chart_json=None
    event_text=None
    slide_no = None
    if request.method == 'POST':
        event_name = request.form["event_name"]
        slide_no = request.form["china_slide_no"]

    try:
        file_name = event_name.lower() +"_"+ slide_no+".txt"
        load_file_name = os.path.join(utility.get_this_dir(),"data","china_trade",file_name)
        print(load_file_name)
        event_text = utility.get_data_from_file(load_file_name)
    except:
        fido="dido"


    if slide_no == "1":
        print("mybozo")
        chart_json = my_altair.get_china_section_1().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            
        #chart_json = my_altair.get_altaire_line_chart_county_trade_for_matrix("China","United States").to_json()
    if slide_no == "2":
        print("mybozo")
        chart_json = my_altair.get_china_section_2().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    if slide_no == "3":
        print("mybozo")
        chart_json = my_altair.get_charts_for_country_dill_down("China","United States",width=350,height=200).to_json()            

    china_slides_total = 2

    return jsonify({'htmlresponse': render_template('modal/china_event.html',event_name=event_name,
    chart_json=chart_json,
    event_text=event_text,
    china_slide_no=slide_no,
    china_slides_total=china_slides_total,)})


@app.route("/render_nafta_graphs",methods=["POST","GET"])
def render_nafta_graphs():
    my_altair = AltairRenderings()
    utility = Utility()
    print("render_nafta_graphs()")
    chart_json=None
    event_text=None
    slide_no = None
    if request.method == 'POST':
        event_name = request.form["event_name"]
        slide_no = request.form["nafta_slide_no"]
    try:
        file_name = event_name.lower() +"_"+ slide_no+".txt"
        load_file_name = os.path.join(utility.get_this_dir(),"data","nafta_trade",file_name)
        print(load_file_name)
        event_text = utility.get_data_from_file(load_file_name)
    except:
        fido="dido"


    if slide_no == "1":
        print("mybozo")
        #chart_json = my_altair.get_nafta_section_1_1().configure_axis(
        chart_json = my_altair.get_nafta_section_1a().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    if slide_no == "2":
        print("mybozo")
        chart_json = my_altair.get_nafta_section_1_1().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    if slide_no == "3":
        print("mybozo")
        chart_json = my_altair.get_nafta_section_2_1().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    
    if slide_no == "4":
        print("mybozo")
        chart_json = my_altair.get_nafta_section_3_1().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()                    

    nafta_slides_total = 4

    return jsonify({'htmlresponse': render_template('modal/nafta_event.html',event_name=event_name,
    chart_json=chart_json,
    event_text=event_text,
    nafta_slide_no=slide_no,
    nafta_slides_total=nafta_slides_total,)})

@app.route("/render_eu_graphs",methods=["POST","GET"])
def render_eu_graphs():
    my_altair = AltairRenderings()
    utility = Utility()
    print("render_eu_graphs()")
    event_name = "JCPOA"
    chart_json=None
    event_text=None
    slide_no = None
    if request.method == 'POST':
        event_name = request.form["event_name"]
        slide_no = request.form["eu_slide_no"]

    try:
        file_name = event_name.lower() +"_"+ slide_no+".txt"
        load_file_name = os.path.join(utility.get_this_dir(),"data","eu_trade",file_name)
        print(load_file_name)
        event_text = utility.get_data_from_file(load_file_name)
    except:
        fido="dido"


    if slide_no == "1":
        print("mybozo")
        chart_json = my_altair.get_eu_section_2().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    if slide_no == "2":
        print("my_altair.get_eu_section_2()")
        chart_json = my_altair.get_eu_section_1().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    if slide_no == "3":
        print("mybozo")
        chart_json = my_altair.get_eu_section_1a().configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).to_json()            

    eu_slides_total = 3

    return jsonify({'htmlresponse': render_template('modal/eu_event.html',event_name=event_name,
    chart_json=chart_json,
    event_text=event_text,
    eu_slide_no=slide_no,
    eu_slides_total=eu_slides_total,)})


@app.route("/videomodaldata",methods=["POST","GET"])
def render_video_modal():
    return jsonify({'htmlresponse': render_template('modal/video_modal.html')})


@app.route("/mapmodaldata",methods=["POST","GET"])
def ajaxfile():

    my_altair = AltairRenderings()

    title = ""
    source_country = "United States"
    target_country = "World"
    if request.method == 'POST':
        source_country = request.form["source_country"].strip()
        target_country = request.form["target_country"].strip()
    print("source_country=", source_country)
    print("target_country=", target_country)
    if target_country.lower() == "world":        
        title = "Trade between <b>" + source_country + "</b> and <b>" + target_country + "</b> top 20 trading nations. To see trade with another country select from drop-down: "
        print("source_country='{}'".format(source_country))
        print("target_country=", target_country)
        chart_json = my_altair.get_charts_for_click_from_world_map(source_country,width=350,height=200).to_json()
        #chart_json = my_altair.get_charts_for_click_from_world_map("Russia",width=350,height=200).to_json()
        form = CountryToWorldVisualizationFormWithWorld(request.form,current_source_country=source_country) 
        return jsonify({'htmlresponse': render_template('modal/modal_chart.html',visualization_form=None,chart_json = chart_json,form=form,source_country=source_country,current_target_country=target_country,country_list=None,modal_title=escape(title))})

    if target_country.lower() !="world":
        title = "Trade between <b>" + source_country + "</b> and <b>" + target_country + "</b>. To see <b>" + source_country +"'s trade with another country select from drop-down: "
        chart_json = my_altair.get_charts_for_country_dill_down(source_country,target_country,width=350,height=200).to_json()
        form = CountryToWorldVisualizationFormWithWorld(request.form,current_source_country=source_country) 
        return jsonify({'htmlresponse': render_template('modal/modal_chart_source_target.html',visualization_form=None,chart_json = chart_json,form=form,source_country=source_country,target_country=target_country,country_list=None,modal_title=escape(title))})

        #"modal_chart_source_target.html"
 




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
    #app.run()
    app.run(host='0.0.0.0')

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

    # with app.app_context():
    #     msg = Message(subject="Hello",
    #                   sender=app.config.get("MAIL_USERNAME"),
    #                   recipients="don.irwin@berkeley.edu".split(), # replace with your email for testing
    #                   body="This is a test email I sent with Gmail and Python!")
    #     mail.send(msg)    
