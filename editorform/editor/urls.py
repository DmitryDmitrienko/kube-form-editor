#coding=UTF-8
__author__ = "Dmitry Dmitrienko"
__copyright__ = "Copyright 2014(c), Dmitry Dmitrienko"
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Dmitry Dmitrienko"
__email__ = "dmitry.dmitrienko@outlook.com"

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .view.views import MainView, CreateFormView, AuthenticateView, UpdateFormView, DeleteFormView, ShareView, \
    FormEditorView, \
    CreateUserView, ChangeUserView
from .view.ajax.elements import ElementCollectionAjaxView, ElementSingleAjaxView


url_editor = patterns('',
                      url(r'^login$', AuthenticateView.as_view(), name='login'),
                      url(r'^logout$', 'editor.view.views.logout', name='logout'),
                      url(r'^$', login_required(MainView.as_view()), name="index"),
                      url(r'^createform$', login_required(CreateFormView.as_view()), name='createform'),
                      url(r'^updateform/(?P<form_id>\d+)$', login_required(UpdateFormView.as_view()),
                          name='updateform'),
                      url(r'^deleteform/(?P<form_id>\d+)$', login_required(DeleteFormView.as_view()),
                          name='deleteform'),
                      url(r'^share/(?P<form_id>\d+)$', login_required(ShareView.as_view()), name='share'),
                      url(r'^form/(?P<form_id>\d+)/$', login_required(FormEditorView.as_view()), name='form'),
                      url(r'^updateuser', login_required(ChangeUserView.as_view()), name='updateuser'),
                      url(r'^createuser$', CreateUserView.as_view(), name='createuser'),
                      #ajax
                      url(r'^form/(?P<form_id>\d+)/ajax/elementcollection',
                          ElementCollectionAjaxView.as_view(), name='elementcollection'),
                      url(r'^form/(?P<form_id>\d+)/ajax/element/(?P<element_id>\d+)',
                          ElementSingleAjaxView.as_view(), name='elementsingle')

)