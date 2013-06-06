$(function() {
    $( "form" ).on( "submit", function( event ) {
        event.preventDefault();
        var data = $(this).find('textarea').val();
        var results = $(this).parent().find('.results');

        $.ajax("/aacore/sparql/", {
            headers: { 
                Accept: "application/sparql-result+json",
            },
            type: "POST",
            contentType: 'application/sparql-query',
            //accepts: {
                //json: 'application/sparql-result+json',
            //},
            dataType: 'json',
            data: data,
            beforeSend: function () {
                console.log('before');
            },
            success: function (data) {
                console.log('success');
                console.log(data);
                var key = data.head.vars[0];
                results.empty();
                for (var i = 0; i < data.results.bindings.length; i++) {
                    results.append('<li><audio src="' + data.results.bindings[i][key].value + '" controls></audio></li>');
                    results.append('<li>' + '<input type="radio" name="foo"/>' + data.results.bindings[i][key].value + '</li>');
                    results.append('<li><img src="' + data.results.bindings[i]['spectro'].value + '" /></li>');
                };
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log("An error occured: " + xhr.status + " " + thrownError);
            },
            complete: function () {
                console.log('complete');
            }
        });
    });
});
