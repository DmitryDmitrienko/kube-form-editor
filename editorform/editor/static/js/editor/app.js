/**
 * Created by Dmitry Dmitrienko on 30.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var app = app || {};

$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    app.editorView = new ElementsEditorView();
    var el = $('#draggable').find('li');
    el.draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid"
    });
    $('#sortable').sortable({
        revert: true,
        stop: function (event, ui) {
            var type = $(ui.item).attr("type");
            if (ui.item.attr('type') != undefined) {
                app.editorView.addElement(type);
                $(ui.item).remove();
            }
            app.editorView.sort();
            $(".dialogScript").remove();
        }
    });
    $("#viewForm").click(function () {
        //$(this).find('form').remove();
        var viewForm = new TemplateFormView({
            coll: app.editorView.coll
        });
        viewForm.setColl(app.editorView.coll);
        viewForm.render();
    });
});