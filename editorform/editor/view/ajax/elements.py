#coding=UTF-8
__author__ = "Dmitry Dmitrienko"
__copyright__ = "Copyright 2014(c), Dmitry Dmitrienko"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Dmitry Dmitrienko"
__email__ = "dmitry.dmitrienko@outlook.com"
import json

from django.views.generic.edit import ProcessFormView
from django.views.generic.edit import DeletionMixin

from .response import ErrorAjaxResponse, SuccessAjaxResponse
from editor.models import FormModel, ElementForm


def element_to_ajax(element):
    data = {
        'idServer': element.id,
        'label': element.label,
        'type': element.type_element,
        'name': element.name,
        'width': element.width,
        'description': element.description
    }
    if (element.type_element == 'input'):
        data.update({
            'typeInput': element.type_input
        })
    elif (element.type_element == 'select'):
        data.update({
            'selectOptions': element.options.split('\n')
        })
    return data


class ElementCollectionAjaxView(ProcessFormView):
    def get(self, request, *args, **kwargs):
        try:
            form_id = kwargs['form_id']
            elements = ElementForm.objects.filter(form=FormModel.objects.get(id=form_id))
            return SuccessAjaxResponse(data=[element_to_ajax(e) for e in elements])
        except Exception as e:
            print e.message
            return ErrorAjaxResponse()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        form_id = kwargs['form_id']
        if 'typeInput' in data:
            t = data['typeInput']
            del data['typeInput']
            data.update({
                'type_input': t
            })
        del data['idServer']
        data['number'] = int(data['number'])
        data['width'] = int(data['width'])
        data = data.dict()
        try:
            element = ElementForm.objects.create(
                form=FormModel.objects.get(id=form_id),
                **data
            )
            return SuccessAjaxResponse(data={'idServer': element.id})
        except Exception as e:
            print e.message
            return ErrorAjaxResponse(e.message)


class ElementSingleAjaxView(ProcessFormView, DeletionMixin):
    def put(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body)
            element_id = kwargs['element_id']
            form_id = kwargs['form_id']
            element = ElementForm.objects.get(id=element_id).update(**data)
            return SuccessAjaxResponse()
        except Exception as e:
            print e.message
            return ErrorAjaxResponse()

    def delete(self, request, *args, **kwargs):
        try:
            element_id = kwargs['element_id']
            ElementForm.objects.get(id=element_id).delete()
            return SuccessAjaxResponse()
        except Exception as e:
            print e.message
            return ErrorAjaxResponse()