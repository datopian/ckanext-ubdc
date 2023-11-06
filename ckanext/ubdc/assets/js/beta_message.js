ckan.module('beta-message', function (jQuery) {
    return {
        initialize: function () {
            // message with cross to close and save on cookiee
            var message = '<div class="beta-message-content">This is a beta version of the UBDC Data Catalog. Please <a href="mailto:ubdc-dataservice@glasgow.ac.uk">contact us</a> if you have any feedback.</div>'
            // append message to the page
            var close = '<button class="beta-message-close" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
            message = message + close 
            var cookie = document.cookie;
            if (cookie.indexOf('beta-message') === -1) {
                jQuery(this.el).html(message);
            }
            var close = document.querySelector('.beta-message-close');

            close.addEventListener('click', function () {
                document.cookie = 'beta-message=true; path=/';
                var message = document.querySelector('.beta-message');
                message.parentNode.removeChild(message);
            });
     
        }

    };

})
