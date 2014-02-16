/**
 * Created by Dmitry Dmitrienko on 29.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var ElementModel = Backbone.Model.extend({
    defaults: {
        idServer: -1,
        name: 'name',
        width: 70,
        description: '-',
        type_element: 'input',
        label: 'Name',
        number: -1

    },
    initialize: function () {
    }
});

var InputElement = ElementModel.extend({
    initialize: function () {
        this.attributes.typeInput = 'text';
    }

});

var CheckBoxElement = ElementModel.extend({
    initialize: function () {
        this.attributes.type_element = 'checkbox';
    }
});

var SelectElement = ElementModel.extend({
    initialize: function () {
        this.attributes.type_element = 'select';
        this.attributes.selectOptions = [];
    }
});

var ElementCollection = Backbone.Collection.extend({
    model: ElementModel
});
