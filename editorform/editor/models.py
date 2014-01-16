from django.db import models
from django.contrib.auth.models import User


class FormModel(models.Model):
    name = models.CharField(max_length=60, verbose_name=u'name form')
    user = models.ForeignKey(User, verbose_name=u'user form')
    created = models.DateField(auto_now_add=True, verbose_name=u'date created')

    def __unicode__(self):
        return self.name


class ElementForm(models.Model):
    type_element = models.CharField(max_length=20, verbose_name=u'type element form')
    label = models.CharField(max_length=60, verbose_name=u'label element')
    description = models.CharField(max_length=120, verbose_name=u'description element')
    width = models.IntegerField(verbose_name=u'width element')
    name = models.CharField(max_length=20, verbose_name=u'name element')
    form = models.ForeignKey(FormModel, verbose_name=u'form of element')

    def __unicode__(self):
        return u'%s type: %s' % (self.form.name, self.type_element)