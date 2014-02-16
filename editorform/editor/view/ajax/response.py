# coding=utf-8
"""
ajax

@author: Дмитриенко Дмитрий
"""
from django.utils import simplejson
from django.http import HttpResponse


class AjaxResponse(HttpResponse):
    """
    Класс ответа по протоколу
    """
    content_type = "application/json"

    def __init__(self, success=True, data=None, message=None, **kwargs):
        """

        @param success:
        @param data:
        @param message:
        @param kwargs:
        """
        response = dict(success=success)
        if data is not None:
            response['data'] = data
        if message is not None:
            response['message'] = message

        response.update(**kwargs)

        super(AjaxResponse, self).__init__(simplejson.dumps(response, ensure_ascii=False),
                                           self.content_type)


class SuccessAjaxResponse(AjaxResponse):
    def __init__(self, data=None, **kwargs):
        super(SuccessAjaxResponse, self).__init__(success=True, data=data, **kwargs)


class ErrorAjaxResponse(AjaxResponse):
    def __init__(self, message=u'Error ajax response', **kwargs):
        super(ErrorAjaxResponse, self).__init__(success=False, message=message, **kwargs)


class AjaxResponseMixin(object):
    """
    Работа с данными для json формата
    """

    def render_to_json_response(self, context, **kwargs):
        """
        Преобразование данных в json формат и ответ клинету
        @param context: контекстные данные ответа
        @param kwargs: dict аргументов
        @return: Ответ клинету в формате json
        @rtype: HttpResponse
        """
        data = simplejson.dumps(context, ensure_ascii=False)
        return HttpResponse(data, mimetype="application/json", **kwargs)