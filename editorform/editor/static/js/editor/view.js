/**
 * Created by Dmitry Dmitrienko on 30.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var ElementView = Backbone.View.extend({
    template: $('#elementTmp').html(),
    events: {
        'click .del-element': 'deleteElement'
    },
    initialize: function () {
        this.listenTo(this.model, 'change', this.render);
        this.listenTo(this.model, 'destroy', this.remove);
    },
    render: function () {
        var templ = _.template(this.template);
        var view = templ(this.model.toJSON());
        this.$el.html(view);
        return this.$el;
    },
    deleteElement: function () {
        this.model.destroy();
    }
});

var ElementsEditorView = Backbone.View.extend({
    el: $("#sortable"),
    initialize: function () {
        this.coll = new ElementCollection();
        this.listenTo(this.coll, 'add', this.addOne);
    },

    addElement: function (type) {
        if (type === 'text') {
            this.coll.add(new InputElement());
        }
        else if (type === 'checkbox') {
            this.coll.add(new CheckBoxElement());
        }
        else if (type === 'select') {
            this.coll.add(new SelectElement());
        }
        else {
            //
        }
    },

    addOne: function (model) {
        var view = new ElementView({model: model});
        this.$el.append(view.render());
    }

});