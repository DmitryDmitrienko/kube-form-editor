/**
 * Created by Dmitry Dmitrienko on 29.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var ElementModel = Backbone.Model.extend({
    defaults: {
        name: 'name',
        width: 100,
        description: '-',
        type: 'input',
        label: 'Name',
        number: -1

    },
    initialize: function () {
    },
    validate: function (attrs) {

    }
});

var InputElement = ElementModel.extend({
    defaults: {
        typeInput: 'text'
    }

});

var CheckBoxElement = ElementModel.extend({
    constructor: function () {
        this.type = 'checkbox';
    }
});

var ElementCollection = Backbone.Collection.extend({
    model: ElementModel
});
