/**
 * Created by Dmitry Dmitrienko on 30.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var ElementView = new Backbone.View.extend({
    tagName: 'div',
    className: 'toggle',
    events: {
        'click .del-element': 'deleteElement'
    },
    initialize: function () {
        this.template = _.template($('#elementTmp').html());
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.render);
    },
    constructor: function () {
        $('#sortable').sortable(this.sortableElement);
    },
    render: function () {
        var view = this.template(this.model.toJSON());
        this.$el.html(view);
    },
    deleteElement: function () {
        this.model.destory();
    },
    sortableElement: {
        revert: true,
        receive: function (event, ui) {
            var html = [];
            $(this).find('li').each(function () {
                html.push('<p class="toggle">' + $(this).html() + '</p>');
            });
            $(this).find('li').replaceWith(html.join(''));
        }
    }
});