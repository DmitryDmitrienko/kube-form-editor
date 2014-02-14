/**
 * Created by Dmitry Dmitrienko on 29.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var ElementModel = Backbone.Model.extend({
    defaults: {
        name: 'name',
        width: 70,
        description: '-',
        type: 'input',
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
        this.attributes.type = 'checkbox';
    }
});

var SelectElement = ElementModel.extend({
    initialize: function () {
        this.attributes.type = 'select';
        this.attributes.selectOptions = ['value1','value2'];
    }
});

var ElementCollection = Backbone.Collection.extend({
    model: ElementModel
});
