/**
 * Created by Dmitry Dmitrienko on 30.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var app = app || {};

$(document).ready(function () {
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
//            var html = [];
//            $(this).find('li').each(function () {
//                html.push('<p class="toggle">' + $(this).html() + '</p>');
//            });
//            $(this).find('li').replaceWith(html.join(''));
            if (ui.item.attr('type') != undefined) {
                app.editorView.addElement(type);
                $(ui.item).remove();
            }
        }
    });
});