$('.site-search button').click(function(event) {
    $('#field-sitewide-search').addClass('');
});

// toggle view full or
$('.view_more_fields').click(function(event) {
    event.preventDefault();
    // get attr
    var count = $(this).attr('data-total-fields');
    $('.repeated_dataset_fields').toggleClass('more');
    $('.card.more').toggleClass('hidden')
    // change text
    if ($('.repeated_dataset_fields').hasClass('more')) {
        $(this).text("View less.");
    }
    else {
        $(this).text(`View ${count - 5} more.`);
    }
});
