/**
 * Created by Dmitry Dmitrienko on 30.01.14.
 * dmitry.dmitrienko@outlook.com
 */
var DialogEditorView = Backbone.View.extend({
    template: $('#dialogTmp').html(),
    events: {
        'click .btnModal': 'closeDialog'
    },
    initialize: function () {
        $(".dialogScript").remove();
    },
    render: function () {
        var templ = _.template(this.template);
        var view = templ(this.model.toJSON());
        this.$el.html(view);
        return this.$el;
    },
    closeDialog: function () {
        this.model.set({
            name: $("#textName").val(),
            width: $("#widthValue option:selected").text(),
            description: $("#textDescription").val(),
            label: $("#textLabel").val()
        });
        if (this.model.attributes.type_element === 'input') {
            this.model.set({
                typeInput: $("#typeInput option:selected").text()
            });
        }
        if (this.model.attributes.type_element === 'select') {
            var arrayOptions = $("#options").val().split('\n');
            console.log(arrayOptions);
            for (var option in arrayOptions) {
                this.model.set({
                    selectOptions: arrayOptions
                })
            }
        }
        $("#myModal").dialog('close');
        $(".dialogScript").remove();
    }
});
var ElementView = Backbone.View.extend({
    template: $('#elementTmp').html(),
    events: {
        'click .del-element': 'deleteElement',
        'click .element': 'modalDialog'
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
        var self = this;
        $.ajax({
                data: {},
                dataTypeString: 'json',
                success: function (data) {
                    if (data.success === true) {
                        self.model.destroy();
                    }
                },
                type: "DELETE",
                url: "ajax/element/" + this.model.attributes.idServer
            });
    },
    modalDialog: function () {
        var dlg = new DialogEditorView({model: this.model});
        $("#myModal").prepend(dlg.render());
        $('#myModal').dialog({
            height: 400,
            width: 500,
            modal: true,
            resizable: true,
            dialogClass: 'no-close success-dialog',
            close: function (e, ui) {
                $(".dialogScript").remove();
            },
            position: { my: "left top", at: "left bottom", of: "#draggable" }
        });
    }
});

var ElementsEditorView = Backbone.View.extend({
    el: $("#sortable"),
    initialize: function () {
        this.coll = new ElementCollection();
        this.listenTo(this.coll, 'add', this.addOne);
        var self = this;
        $.ajax({
            data: '',
            dataTypeString: 'json',
            success: function (data) {
                if (data.success === true) {
                    var data = data.data;
                    for (var i = 0; i < data.length; i++) {
                        self.coll.add(self.addDataElement(data[i]));
                    }
                }
            },
            type: "GET",
            url: "ajax/elementcollection"
        });
    },

    addElement: function (type) {
        var self = this;
        var element = this.newElement(type);
        $.ajax({
            data: element.toJSON(),
            dataTypeString: 'json',
            success: function (data) {
                if (data.success === true) {
                    var data = data.data;
                    id_element = data.idServer;
                    if (id_element > 0) {
                        element.set({
                            idServer: id_element
                        });
                        self.coll.add(element);
                    }
                }
            },
            type: "POST",
            url: "ajax/elementcollection"
        });
    },

    newElement: function (type) {
        if (type === 'text') {
            return new InputElement();
        }
        else if (type === 'checkbox') {
            return new CheckBoxElement();
        }
        else if (type === 'select') {
            return new SelectElement();
        }
        else {
            console.log("unknown type");
            return {};
        }
    },
    addDataElement: function (data) {
        if (data.type === 'input') {
            return new InputElement(data);
        }
        else if (data.type === 'checkbox') {
            return new CheckBoxElement(data);
        }
        else if (data.type === 'select') {
            return new SelectElement(data);
        }
        else {
            console.log("unknown type");
            return {};
        }
    },
    addOne: function (model) {
        var view = new ElementView({model: model});
        this.$el.append(view.render());
        $(".dialogScript").remove();
    },
    sort: function () {
        $(".toggle").each(function (index, value) {
            $(this).attr("number", index + 1);
        });
    }

});

var TemplateFormView = Backbone.View.extend({
    template: $('#formTmp').html(),
    render: function () {
        console.log(this.coll);
        var templ = _.template(this.template);
        var view = templ({elements: this.coll.toJSON()});
        this.$el.html(view);
        $("#formBody").val(view);
    },
    setColl: function (collecction) {
        this.coll = collecction;
    }
});