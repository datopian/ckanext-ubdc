ckan.module("data-service-request-form", function (jQuery) {
    return {
        initialize: function () {
            var message = this._('There are unsaved modifications to this form');

            $.proxyAll(this, /_on/);

            this.el.incompleteFormWarning(message);

            // Disable the submit button on form submit, to prevent multiple
            // consecutive form submissions.

            this.el.on('submit', this._onSubmit);

            this.el.find('.checkboxes label').click(function (event) {
                event.stopPropagation();
                var checkbox = $(this).find('input');
                checkbox.prop('checked', !checkbox.prop('checked'));
            });
            
            this.el.find('.checkboxes label input').click(function (event) {
                event.stopPropagation();
            });
        },
        _onSubmit: function () {
            // The button is not disabled immediately so that its value can be sent
            // the first time the form is submitted, because the "save" field is
            // used in the backend.

            var consent = this.el.find('input[name="consent"]')
            var contactConsent = this.el.find('input[name="contactConsent"]')
            if (!consent.prop('checked')) {
                consent.attr('required', true);
                return false; 
            }
            if (!contactConsent.prop('checked')) {
                contactConsent.attr('required', true);
                return false;
            }
                    
            setTimeout(function () {
                this.el.find('button[name="save"]').attr('disabled', true);
            }.bind(this), 0);
        }
    };
});