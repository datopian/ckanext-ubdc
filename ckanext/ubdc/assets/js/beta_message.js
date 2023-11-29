ckan.module('beta-message', function (jQuery) {
    return {
        initialize: function () {
            // message with cross to close and save on cookiee
            var message = '<div class="beta-message-content">Welcome to our new Data Catalogue. This site is still in BETA mode. If you experience issues or have questions <a href="mailto:ubdc-dataservice@glasgow.ac.uk">please get in touch</a>.</div>'
            // append message to the page
            var close = '<button class="beta-message-close" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
            message = `<div class="beta-message"> ${message} ${close} </div>`
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
