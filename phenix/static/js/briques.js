if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}


$(function() {
    var composition = $('#composition');
    var imgUrl = [
        "http://localhost:8000/media/spectrograms/fb0afcdf443e3a1528595176c9729373825c7679.png",
        "http://localhost:8000/media/spectrograms/37431065c2b8dbfc0d9993c1a4c556a0bd73ad2c.png",
        "http://localhost:8000/media/spectrograms/cdb26b17b8b019fbdc1f201db93e13cce2b0956d.png",
        "http://localhost:8000/media/spectrograms/39c2beea50f9dfea13d8350fdce5d08b07666b1a.png",
        "http://localhost:8000/media/spectrograms/758801712c8248e8e7405ada2a15a181e847f44e.png",
        "http://localhost:8000/media/spectrograms/135039dda8d3e2dd98a77e7a27601b396c7bb77c.png",
        "http://localhost:8000/media/spectrograms/d49c2cfd945400e6d1e9491666f8cd0710310c8b.png",
        "http://localhost:8000/media/spectrograms/2045bb8a7ebbc4c43f031ec12414e22ecea2dae6.png",
        "http://localhost:8000/media/spectrograms/74c33d0cbc386b8e45215931fd59588b0740f938.png",
        "http://localhost:8000/media/spectrograms/32c0d5203b58ed39e4774747409af647e45ade55.png",
        "http://localhost:8000/media/spectrograms/fc09b42ad40f8dc3ca905201286ec1b62fb1cc01.png"
    ]

    $('.icon-reload').on('click', function() {
        var i = Math.floor(Math.random() * imgUrl.length);
        $(this).parents('.briq').find('img').attr('src', imgUrl[i]);
    });

    var cbfunc = function(results) {
        $.each(results.results.bindings, function(index, value) {
            var ctx = {
                'title': value['title'].value,
                'resource': value['resource'].value,
                'spectrogram': value['spectrogram'].value
            };

            var tmpl = $('#brick-tmpl').html();
            composition.append(_.template(tmpl, ctx));
        });
    };

    var query = function() {
        var q = $.sparql("/sparql/", {method: 'POST'})
            .prefix("aa","http://activearchives.org/terms/")
            .prefix("dc","http://purl.org/dc/elements/1.1/")
            .select(["?title"])
            .where("?s","aa:nature",'"parole"@fr')
            .where("?s","dc:title","?title")
            .execute(cbfunc);
    };


    var parseQuery = function(query) {
        var tree = [];
        var bricks = query.split('+');

        $.each(bricks, function(index, value) {
            value = value.trim();

            var statements = value.split('&');

            var d = {};
            $.each(statements, function(index, value) {
                value = value.trim();

                var i = value.indexOf(':')
                var key = value.substring(0, i)
                var value = value.substring(i + 1)

                d[key] = value;
            });
            tree.push(d);
        });

        return tree
    };

    $('#btn-compose').on('click', function() {
        composition.empty();

        var query = $('textarea').val();
        var tree = parseQuery(query);

        $.each(tree, function(index, value) {
            // new query
            var q = $.sparql("/sparql/", {method: 'POST'})
                .prefix("aa","http://activearchives.org/terms/")
                .prefix("dc","http://purl.org/dc/elements/1.1/")
                .select(["?resource", "?title", "?spectrogram"])
                .distinct()
                .where("?resource","dc:title","?title")
                .where("?resource", "aa:spectrogram", "?spectrogram");

            $.each(value, function(key, value) {
                q.where("?resource","aa:" + key ,'"' + value + '"@fr')
            });

            q.execute(cbfunc);
        });
    });

});
