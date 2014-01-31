/**
 * Created by Dmitry Dmitrienko on 30.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var app = app || {};

$(document).ready(function () {
    var el = $('#draggable').find('li');
    el.draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid"
    });
    app.editorView = new ElementView({
        el: "#sortable"
    });
});