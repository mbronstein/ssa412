from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django_extensions.db.fields import AutoSlugField
import os
import uuid
import pypdftk
import time



class FormRenderException (Exception):
    pass



def time_in_seconds():
    """return time in seconds since midnight local time"""
    t = time.localtime()
    return t.tm_hour * 3600 + t.tm_min*60 + t.tm_sec



# combo of mimetype and template_type determines the type of merge_template to use

mimetype_choices = (('pdf', 'pdf'), ('docx','docx'), ('txt', 'txt'), ('html', 'html'), ('xlsx', 'xlsx'))
#type of renderer

template_type_choices = (('pdf','pdf'), ('reportlab', 'reportlab'), ('docx', 'docx'))
category_choices = (('ss_form','ss form'), ('sso_letter','sso letter'),('gen_letter','gen letter'),
                         ('ins_letter','ins letter'), ( 'med_rec_req', 'med rec req'),
                         ('lomb_form', 'lomb_form')
                         )

class MergeForm(models.Model ):

    sysid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True )
    name = models.CharField(max_length=90, unique=True)
    uuid =models.CharField( max_length=50,
                          unique=True,
                          )
    mimetype = models.CharField(choices=mimetype_choices,
                                max_length=20)
    category = models.CharField(choices=category_choices,
                                     max_length=20,
                                     null=True)
    template_type = models.CharField(choices=template_type_choices,
                                     max_length=20)
    filename = models.CharField(max_length=120,
                                blank=True, null=True)
    repo = models.CharField(max_length=10, blank=True, default="mergeforms")

    description =  models.CharField(max_length=90,
                                    blank=True,
                                    null=True)
    tags = TaggableManager()
    comments = models.TextField(blank=True, null=True)
    text_body = models.TextField(blank=True,
                                 null=True)
    blob_body = models.BinaryField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='+',
                                   null=True,
     )
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='+',
                                         null=True,
    )

    #repo related: where is the template file stored?
    @property
    def repo_root(self):
        return settings.REPOS[self.repo]['root']

    @property
    def repo_url(self):
        return settings.REPOS[self.repo]['url']

    @property
    def filepath(self):
        return os.path.join(settings.REPOS[self.repo]["root"],self.filename)

    @property
    def url(self):
        return os.path.join(settings.REPOS[self.repo]["url"],self.filename)


    def __str__(self):
        return self.name


    def render(self,
               field_dict=None,
               output_filename = None,
               output_dirpath=None,
               flatten=False):

        if output_filename is None:
            output_filename = "{0}_{1}_{2}.{3}".format(field_dict["claimant.last_name"],
                                     self.uuid,
                                     str(time_in_seconds()),
                                     self.mimetype
                                     )
        if output_dirpath is None:
            output_dirpath = os.path.join(settings.BASE_DIR, "temp")
            if not os.path.exists(output_dirpath):
                try:
                    os.mkdir(output_dirpath)
                except:
                    raise Exception("Creation of the directory {0} failed".format(output_dirpath))

        if self.mimetype == 'pdf':
            generated_output_path = pypdftk.fill_form(self.filepath,
                                                      field_dict,
                                                      os.path.join(output_dirpath, output_filename)
                                                      )


            return generated_output_path
        elif self.template_type == 'docx':
            pass
        elif self.template_type == 'xlsx':
            pass
        else:
            pass

