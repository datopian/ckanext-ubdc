$('.site-search button').click(function(event) {
    $('#field-sitewide-search').addClass('');
});

// toggle view full or
$('.view_more_fields').click(function(event) {
    event.preventDefault();
    $('.repeated_dataset_fields').toggleClass("more");
    // change text
    if ($('.repeated_dataset_fields').hasClass("more")) {
        $(this).text("View less");
    }
    else {
        $(this).text("View more");
    }
});
