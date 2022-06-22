# -*- coding: utf-8 -*-
"""form.py"""

from cms10.settings import Config
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import class_mapper

from flask import make_response, url_for

from cms10.initdb import db


from flask_marshmallow import Schema

import os
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
from tempfile import TemporaryFile


form_tag_association_table = db.Table('form_tag_association_table',
                             db.Column('merge_form_id', db.Integer,
                                       db.ForeignKey('merge_forms.id'),
                                       nullable=False),
                             db.Column('tag_id', db.Integer,
                                       db.ForeignKey('form_tags.id'),
                                       nullable=False)
                             )


class MergeForm(db.Model):
    __tablename__ = 'merge_forms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    filename = db.Column(db.String(50))
    foldername = db.Column(db.String(50))
    mimetype = db.Column(db.String(30))
    # fields = db.relationship('FormField',
    #                        collection_class=attribute_mapped_collection("name"),
    #                         backref='form_field')
    comments = db.Column(db.Text())
    created_by = db.Column(db.String(10))
    last_modified = db.Column(db.DateTime())
    tags = db.relationship('Tag',
                           secondary = form_tag_association_table,
                           backref='merge_forms')

    def __repr__(self):
        return self.name

    def get_field_list(self):
        """return list of all model fields, including calculated 'hybrid' fields"""
        prop_list =  class_mapper(MergeForm).all_orm_descriptors.keys()
        prop_list.remove('__mapper__')
        return prop_list


    def as_json(self):
        """return mergeform as json """
        fld_list = self.get_field_list()
        retdict = {}
        for fldname in fld_list:
            try:
                fld_val = getattr(self, fldname)
                if fld_val:
                    retdict[fldname] = fld_val
            except AttributeError:
                print('Error: ' + fldname +' not found.')
        try:
            if self.last_modified:
                retdict[u'last_modified']  = self.last_modified.isoformat()
        except Exception:
            print "Error. No last_modified field to convert to string"
        retdict[u'id'] = unicode(self.id)
        retdict[u'href'] = url_for('api_bp.get_form', form_id=self.id, _external=True)
        retdict[u'text']  = self.name
        if self.tags:
            retdict[u'tags'] = [tag.name for tag in self.tags]
        # add links for subrecords like phone, email, etc
        return retdict

    @staticmethod
    def get_all_merge_forms():
        return MergeForm.query.order_by('name').all()



class FormField(db.Model):
    __tablename__ = 'form_fields'
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('merge_forms.id'))
    name = db.Column(db.String(30), db.ForeignKey('form_field_list.name'))
    page = db.Column(db.Integer)
    x = db.Column(db.Float(), default=0)
    y = db.Column(db.Float(), default=0)
    value = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return "{0}".format(self.name)


class FormFieldList(db.Model):
    __tablename__ = 'form_field_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    description = db.Column(db.String(30), nullable=True)
    notes = db.Column(db.Text, nullable = True)


# class FormSchema(Schema):
#     class Meta:
#         # Fields to expose
#         fields = ('email', 'date_created', '_links')
#
#     # Smart hyperlinking
#     _links = ma.Hyperlinks({
#         'self': ma.URLFor('author_detail', id='<id>'),
#         'collection': ma.URLFor('authors')
#     })
#
#
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
#


class Tag(db.Model):
    __tablename__ = 'form_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False, )
    description = db.Column(db.Text)

    def __repr__(self):
        return self.name

def getFormsByTag( tag):
        if not tag:
            return MergeForm.query.order_by(Tag.name).all()
        else:
            q = db.session.query(MergeForm)
            q = q.filter(MergeForm.tags.any(Tag.name == tag))
            return q.all()