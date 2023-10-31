ckan.module("data-service-request-form", function (jQuery) {
    return {
        initialize: function () {
            var message = this._('There are unsaved modifications to this form');

            $.proxyAll(this, /_on/);

            this.el.incompleteFormWarning(message);

            // Disable the submit button on form submit, to prevent multiple
            // consecutive form submissions.
            var button = this.el.find('button[name="save"]')

            var consent = this.el.find('input[name="consent"]')
            if (consent.length > 0) {
                consent.attr('required', true);
            }
            this.el.on('submit', this._onSubmit);

            this.el.find('.checkboxes label').click(function (event) {
                var checkbox = $(event.currentTarget).find('input')
                checkbox.prop('checked', !checkbox.prop('checked'));
            });
        },
        _onSubmit: function () {
            // The button is not disabled immediately so that its value can be sent
            // the first time the form is submitted, because the "save" field is
            // used in the backend.
            setTimeout(function () {
                this.el.find('button[name="save"]').attr('disabled', true);
            }.bind(this), 0);
        }
    };
});