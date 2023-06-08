from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import Table, select, join, MetaData
#from .models import Note, ImageSet, Image
from .models import Virus, Hosts
from . import db #, session
import json
import os
#Import apy.py
from . import api
import collections

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'], endpoint='home')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/hosts', methods=['GET', 'POST'])
@login_required
def hosts():
    print(current_user.id)
    #dataToHtml = api.getHosts(str(current_user.id), "1234567890") #In real
    dataToSend = api.getHosts() # debug for user1
    print(dataToSend)

    return render_template("home.html", user=current_user, dataToHtml = dataToSend)

@views.route('/virus', methods=['GET', 'POST'])
@login_required
def virus():
    print(current_user.id)
    dataToSend = api.getVirus() 
    print(dataToSend)

    return render_template("virus.html", user=current_user, dataToHtml = dataToSend)

    
@views.route('/authtest', methods=['GET', 'POST'])
# @login_required
def authTest():
    return render_template("authtest.html", user=current_user)

