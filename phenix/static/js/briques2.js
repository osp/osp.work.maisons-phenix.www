;$(function() {

    window.ResultModel = Backbone.Model.extend({
        defaults: {
            index: 0,
        },
        random: function () {
            var results = this.get("results").bindings;
            var index = Math.floor(Math.random() * results.length);
            this.set({index: index});
            var result = results[index];

            return result;
        },
        previous: function () {
            return result;
        },
        next: function () {
            return result;     
        }
    });


    window.ResultCollection = Backbone.Collection.extend({
        model: ResultModel
    });


    window.ResultView = Backbone.View.extend({
        tagName: 'audio',
        initialize: function() {
            var that = this;
            this.model.on("change:index", function(model){
                that.render();
            });
            this.render();
        },
        render: function() {
            var model = this.model.random();
            var src = model.resource.value;
            var length = model.length.value;

            return this.$el.attr({
                'src': src,
                'controls': '',
                'data-dur': length + 's'
            });
        }
    });


    window.PlaylistView = Backbone.View.extend({
        el: '#playlist-region',
        template: $('#playlist-tmpl').html(),
        initialize: function() {
            this.$el.html(this.template);
            this.render();
            this.collection.bind("reset", this.render.bind(this));
            this.listenTo(this.collection, 'change:index', function() { console.log("ok"); });
            //this.collection.bind('change:index', function(model) { console.log("blabl") });
            window.collection = this.collection;
        },
        render: function() {
            var container = this.$el.find('#playlist');

            container.empty();

            var timing = container.prop('timing');
            if (timing) { timing.reset(); };

            this.collection.each(function(model) {
                var resultView = new window.ResultView({model: model})
                container.append(resultView.$el);
            });

            var t = document.createTimeContainer(container.get(0));
            t.show();

            return this;
        }
    });



    window.OneSpectrogramView = Backbone.View.extend({
        tagName: 'div',
        template: $('#spectrogram-tmpl').html(),
        attributes: {
            'class': 'briq'
        },
        events: {
            'click .icon-reload': 'render',
        },
        initialize: function() {
            this.render();
        },
        render: function() {
            var model = this.model.random();
            var title = model.title.value;
            var spectrogram = model.spectrogram.value;
            this.$el.empty();
            this.$el.append(_.template(this.template, {
                'title': title,
                'spectrogram': spectrogram
            }));
            return this;
        }
    });


    window.SpectrogramView = Backbone.View.extend({
        el: '#spectrogram-region',
        initialize: function() {
            this.collection.bind("reset", this.render.bind(this));
            this.render();
        },
        render: function() {
            console.log('rendering');
            var $el = this.$el;

            this.$el.empty();
            this.collection.each(function(model) {
                var resultView = new window.OneSpectrogramView({model: model})
                $el.append(resultView.$el);
            });

            return this;
        }
    });


    // The view for the texarea
    window.QueryView = Backbone.View.extend({
        el: '#query-region',
        template: $('#query-tmpl').html(),
        events: {
            'click .icon-compose':'doCompose'
        },
        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el
            .empty()
            .html(_.template(this.template, {}));

            return this;
        },
        parseQuery: function(query) {
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
        },
        doCompose: function(event) {
            var query = this.$el.find('textarea').val();
            var tree = this.parseQuery(query);

            var resultModels = [];
            window.resultCollection.reset();

            $.each(tree, function(index, value) {
                var q = $.sparql("/sparql/", {method: 'POST'})
                    .prefix("aa","http://activearchives.org/terms/")
                    .prefix("dc","http://purl.org/dc/elements/1.1/")
                    .select(["?resource", "?title", "?spectrogram", "?length"])
                    .distinct()
                    .where("?resource","dc:title","?title")
                    .where("?resource", "aa:spectrogram", "?spectrogram")
                    .where("?resource", "aa:duration", "?length");

                $.each(value, function(key, value) {
                    q.where("?resource","aa:" + key ,'"' + value + '"')
                });

                q.execute(function(results) {
                    resultModels.push(new ResultModel(results));
                    if (resultModels.length === tree.length) {
                        window.resultCollection.reset(resultModels);
                    };
                });
            });

        }
    });


    // The textarea
    window.queryView = new QueryView();

    // A collection of results, empty until we do the first composition
    window.resultCollection = new ResultCollection();

    // 
    window.playlistView = new PlaylistView({collection: window.resultCollection});
    window.spectrogramView = new SpectrogramView({collection: window.resultCollection});
});

// vim: set foldmethod=indent :
