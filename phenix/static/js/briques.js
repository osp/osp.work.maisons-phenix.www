if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}


$(function() {
    var composition = $('#composition');

    var cbfunc = function(results) {
        var brick = aa.Brick(results);
        var $html = brick.render();
        composition.append($html);
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


window.aa = window.aa || {};


aa.Brick = function(results)
{
    var proto = {
        init: function (results) {
            this.results = results;

            return this;
        },
        pick: function () {
            var bindings = this.results.results.bindings;
            var index = Math.floor(Math.random() * bindings.length);
            var value = bindings[index];
            return value;
        },
        render: function () {
            var tmpl = _.template($('#brick-tmpl').html());
            var value = this.pick();

            var ctx = {
                'title': value['title'].value,
                'resource': value['resource'].value,
                'spectrogram': value['spectrogram'].value
            };

            var $html = $(tmpl(ctx).replace(/^[ \t\n\r]+/gm, ''));

            var that = this;
            $html.find('.icon-reload').on('click', function() {
                $(this).parents('.briq').replaceWith(that.render());
            });

            return $html;
        }
        
    };
    
    return Object.create(proto).init(results);
}


