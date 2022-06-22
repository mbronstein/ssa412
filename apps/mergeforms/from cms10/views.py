# -*- coding: utf-8 -*-
"""Api views."""

import datetime
import os
from time import sleep
from json import dumps, loads
from merge_template_lib import template_factory
from cms10.api_bp.merge_data_extractor import MergeDataExtractor
from cms10.initdb import db
from cms10.models import Contact
from cms10.models import MergeForm
from cms10.models import SSOffice
from cms10.models.mergeform import getFormsByTag
from cms10.settings import Config
from flask import Blueprint, jsonify, send_from_directory
from flask import request
from ..extensions import cache
from model_importer import ModelImporter
from tmdownloader import ConManager
from flask_security import login_required
from flask_cors import cross_origin
from cms10.mbphonenumber_lib import mbPhoneNumber
from sqlalchemy import or_

#  from myapp.ssofficemanager_bp.ssofficemanager import SSOfficeManager

blueprint = Blueprint('api_bp', __name__, url_prefix='/api')


token = u'x'

def authenticate(request, token=token):
    if "token" not in request.args:
      return False
    submitted_token = request.args['token']
    if submitted_token != token:
         return False
    else:
         return True

@blueprint.route('/')
@login_required
def root_api():
    return "API"

# API Endpoint to return jsonified ssofficelist dictionary with lists of FO, DDS and ODAR offices
@blueprint.route('/ssoffices_by_type/')
def get_ssoffice_list_as_json():
    if authenticate(request):
        x = SSOffice.get_ssoffices_by_type_as_dict_list()
        return jsonify(x)
    else:
        return "Authentication Error"


# get SSOffice list, optionally filtered by "type" and then "city" params return list as json
@blueprint.route('/ssoffices/')
# @cache.cached(timeout=500)
def get_ssoffices():
    """get ss office list"""
    try:
        if authenticate(request):
            qry = SSOffice.query.order_by(SSOffice.city)
            if len(request.args) == 0:
                lst = []
                for o in qry.all():
                     lst.append(o.as_dict())
                return jsonify(lst)
            else:
                if 'type' in request.args:
                    typ = request.args['type'].upper()
                    qry = qry.filter(SSOffice.type == typ)
                if 'city' in request.args:
                    cty = request.args['city'].capitalize()
                    qry = qry.filter(SSOffice.city == cty)
            lst = []
            for o in qry.all():
                lst.append(o.as_dict())
            return jsonify(lst)
        else:
            return "Authentication Error"
    except Exception as e:
        return "Error Message", e




# return ssofice by id as json
@blueprint.route('/ssoffices/<id>')
@login_required
@cache.cached(timeout=500)
def get_ssoffice(id):
    """get ss office by id"""
    try:
        office = SSOffice.query.get_or_404(id)
    except Exception as e:
        return "Error Message", e
    return jsonify(office.as_dict())

# CONTACTS

# import contacts from TM online to local sqlite
@blueprint.route('/sync_contacts')
@login_required
def sync_contacts():
    cm = ConManager()
    fn = "contacts_{0}.json".format(datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
    cm.download2JSONFile(os.path.join(Config.APP_DIR, "static"), fn)
    ci = ModelImporter(os.path.join(Config.APP_DIR, "static", fn), db, Contact)
    ci.run_import()
    print("contacts imported")
    print("updating reverse phone lookup file")
    Contact.update_phoneno_lookup_list()
    return "Import complete"

@blueprint.route('/import_contacts')
@login_required
def import_contacts():
    fn = 'contacts.json'
    mydb = db
    ci = ModelImporter(os.path.join(Config.APP_DIR, "static", fn), db, Contact)
    ci.run_import()
    return "Contacts Imported"


@blueprint.route('/contacts/')
# @cache.cached(timeout=500)
def get_contacts():
    """get contact list with optional filtering and optional variable fields"""
    output_fld_list = None
    #if  no request args retrieve all contacts with all fields
    #    else parse args for filters and field list
    try:
        if not authenticate(request):
            return "Authentication Error"
        else:
            if len(request.args) == 1:
                qry = Contact.query.order_by( Contact.last_name,
                                    Contact.first_name,
                                    Contact.middle_name,
                                    Contact.org_name).all()
                # return (o.as_json for o in qry)
                lst = []
                for o in qry:
                    lst.append(o.as_json())
                return jsonify(lst)
            else:
                output_fld_list = None
                if 'fields' in request.args:
                    output_fld_list = request.args['fields'].split(',')
                    output_fld_list.append(u'uri')
                if 'phoneno' in request.args:
                    # if phoneno arg return contacts with matching phone numbers and ignore other params
                    qry = Contact.get_by_phone(request.args['phoneno'])
                    return jsonify(o.as_json() for o in qry)
                if 'lookup_name' in request.args:
                    qry = Contact.filter(Contact.last_name.like(request.args['lookup_name'] + '%')).order_by( Contact.last_name,
                                    Contact.first_name,
                                    Contact.middle_name,
                                    Contact.org_name)
                    return (o.as_json() for o in qry)
    except Exception as e:
        return e.message

@blueprint.route('/contacts/<id>')
@login_required
def get_contact(id):
    output_fld_list = None
    """get contact list"""
    if 'fields' in request.args:
        output_fld_list = request.args['fields'].split(',')
    try:
        contact = Contact.query.get_or_404(id)
        return jsonify(contact.as_json(output_fld_list=output_fld_list))
    except:
        return "Error Message"

@blueprint.route('/contact_choices')
# @cache.cached(timeout=500)
def get_contact_lookup_list():
        """get contact lookup list"""
        try:
            return jsonify(Contact.get_contact_choices())
        except Exception as e:
            return e.message

# Merge Forms


# return a json list of all forms
@blueprint.route('/forms', methods=['GET'])
def get_form_list():
    """get form list"""
    try:
        if not authenticate(request):
            return "Authentication Error"
        else:
            if len(request.args) == 1:  # that is only parameter was the api token
                qry = MergeForm.query.order_by(MergeForm.name).all()
                # return (o.as_json for o in qry)
                lst = []
                for o in qry:
                    lst.append(o.as_json())
                return jsonify(lst)
    except Exception as e:
        return e.message

# get form by id optionally merged with data
@blueprint.route('/forms/<form_id>', methods=['GET'])
def get_form(form_id):
    # retrieve the requested form  model
    mform = MergeForm.query.get_or_404(form_id)
    #create merge_template object from form model properties
    merge_template = template_factory(mform.filename,
                                   os.path.join(Config.FORM_ROOT,
                                   mform.foldername),
                                   Config.FORM_OUTPUT_DIR)
    # if no request args then just return blank form
    field_data_dict = None
    if len(request.args) == 0:
       return send_from_directory( merge_template.form_dirpath, merge_template.form_filename)
    # else assume there is data to merge
    else:
        mde = MergeDataExtractor(request)
        field_data_dict = mde.get_merge_data_dic()
        form_path = merge_template.form_filepath
        outputfp = merge_template.render(field_data_dict)
        sleep(1)
        if not os.path.exists(outputfp):
            return "Output form: {0} not found".format(outputfp)
        else:
            p, f = os.path.split(outputfp)
            return send_from_directory(p, f)

@blueprint.route('/forms/<form_id>/grid', methods=['GET'])
def get_form_with_grid(form_id):
    mform = MergeForm.query.get_or_404(form_id)
    # create merge_template object from mform properties
    if mform.mimetype != 'pdf':
        return "No grid available for non-pdf forms"
    merge_template = template_factory(mform.filename,
                                      os.path.join(Config.FORM_ROOT,
                                                   mform.foldername),
                                      Config.FORM_OUTPUT_DIR,
                                      mform.fields)
    outputfp = merge_template.render_grid()
    p, f = os.path.split(outputfp)
    return send_from_directory(p, f)

