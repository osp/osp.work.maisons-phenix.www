window.AA = window.AA || {};


(function(undefined) {
    'use strict';

    AA.play = function () {
        var playlist = [];
        var el = $('#resource').get(0);
        var src = el.src;
        var current = 0;

        $($('section[data-begin]').get().reverse()).each(function() {
            var begin = parseFloat($(this).data('begin'));
            var end = parseFloat($(this).data('end'));
            playlist.push(src + '#t=' + begin + ',' + end);
        });

        $(el).on('pause', function() {
            this.src = playlist[current];
            this.play();
            current++;
        });

        el.src = playlist[current];
        el.play();
    }

    AA.selected = undefined;
    AA.current = undefined;

    AA.AnnotationModel = Backbone.Model.extend({
        urlRoot: AA.routes.annotationList,
        defaults: {
            body: "Nouvelle annotation",
            top: 10,
            left: 10,
            width: 300,
            height: 400,
            resource: AA.routes.resourceDetail,
        }
    });


    AA.AnnotationCollection = Backbone.Collection.extend({
        model: AA.AnnotationModel,
        urlRoot: AA.routes.annotationList,
    });


    AA.AnnotationView = Backbone.View.extend({
        tagName: 'section',
        templates: {
            view: _.template($('#annotation-view-template').html()),
            edit: _.template($('#annotation-edit-template').html()),
        },
        editing: false,
        events : {
            //'dblclick' : 'toggle',
        },
        onChange: function(model, options) {
            var defaults = {
                animate: false
            };
            var options = $.extend({}, defaults, options);

            if (options.animate === true) {
                this.$el.animate({
                    left: model.changed.left,
                    top: model.changed.top
                }, 2000, 'easeOutExpo');
            };
        },
        initialize: function() {
            var that = this;

            this.listenTo(this.model, 'destroy', this.remove);
            this.listenTo(this.model, 'change', this.onChange);

            marked.setOptions({
                timecode: true,
                semanticdata: 'aa',
            });

            this.$el
            .on('click', function(event) {
                //event.stopImmediatePropagation();
                if (AA.selected) {
                    $(AA.selected).removeClass('selected');
                };
                AA.selected = this;
                $(this).addClass('selected');
            })
            .contextual({
                iconSize: 40,
                iconSpacing: 5,
                onShow: function() {
                    if (AA.current && AA.current !== this) {
                        AA.current.hide();
                    };

                    AA.current = this;
                }
            });

            var btn = $('<div>')
            .attr({
                title: 'edit annotation',
                draggable: false,
                class: 'icon icon7'
            })
            .on('click', function(event) {
                //that.$el.contextual('hide');
                that.toggle();
                return false;
            });

            this.$el.contextual('register', 'click', 'left', btn);

            var btn = $('<div>')
            .attr({
                title: 'delete annotation',
                draggable: false,
                class: 'icon icon6'
            })
            .on('click', function(event) {
                if (window.confirm('This will permanently delete this annotation. Proceed?')) {
                    that.$el.contextual('hide');
                    that.model.destroy();
                };
                return false;
            });

            this.$el.contextual('register', 'click', 'top', btn);


            this.render();
        },
        render: function() {
            if (this.editing) {
                var $textarea = $(this.templates.edit({body: this.model.get("body")}));

                $textarea.bind('keydown', "Ctrl+Shift+down", function timestamp(event) {
                    var currentTime = $('#resource').get(0).currentTime;
                    $textarea.insertAtCaret('\n' + currentTime.secondsTo('hh:mm:ss.ms') + ' -->\n');
                    return false;
                });

                this.$el
                .empty()
                .addClass('editing')
                .append($textarea);
            } else {
                var model = this.model;
                var body = marked(this.model.get("body"));
                var that = this;

                this.$el
                .empty()
                .removeClass('editing')
                .html(this.templates.view({body: body}))
                .addClass('section1')
                .css({
                    width: this.model.get("width"),
                    height: this.model.get("height"),
                    top: this.model.get("top"),
                    left: this.model.get("left"),
                })
                .resizable({
                    resize: function (event, ui) {
                        if (event.ctrlKey) {
                            $("html").addClass("grid");

                            ui.element.width((Math.floor(ui.size.width / 20) * 20) - (ui.position.left % 20));
                            ui.element.height((Math.floor(ui.size.height / 20) * 20) - (ui.position.top % 20));
                        } else {
                            $("html").removeClass("grid");
                        }
                    },
                    stop: function(event, ui) {
                        $("html").removeClass("grid");

                        model.set({
                            'width': ui.size.width,
                            'height': ui.size.height,
                        }).save();
                    }
                })
                .draggable({
                    distance: 20,
                    scroll: true,
                    start: function(event, ui) {
                        that.$el.contextual('hide');
                    },
                    drag: function (event, ui) {
                        if (event.ctrlKey) {
                            $("html").addClass("grid");
                            ui.position.left = Math.floor(ui.position.left / 20) * 20;
                            ui.position.top = Math.floor(ui.position.top / 20) * 20;
                        } else {
                            $("html").removeClass("grid");
                        }
                    },
                    stop: function(event, ui) { 
                        that.$el.contextual('show');
                        $("html").removeClass("grid");

                        // Makes sure an annotation doesn't get a negative
                        // offset
                        var pos = $(this).position();

                        pos.top = pos.top < 0 ? 0 : pos.top;
                        pos.left = pos.left < 0 ? 0 : pos.left;

                        $(this).css({
                            top: pos.top,
                            left: pos.left
                        });

                        model.set({
                            top: pos.top,
                            left: pos.left,
                        }).save();
                    }
                })
                .find("section").each(function() {
                    var $this = $(this),
                        begin = $(this).data('begin'),
                        end = $(this).data('end');

                    //var tmpl = ''
                    //+ '<a href="#t=<%= timecode %>">'
                    //+ '<time property="<%= property %>"><%= timecode %></time>
                    //+ '</a>';

                    //var compiled = 

                    var beginAElt = $('<a>')
                    .attr('href', '#t=' + begin)
                    .on('click', function(event) {
                        event.stopPropagation();
                    })
                    .append(
                        $('<time>')
                        .attr('property', 'aa:begin')
                        .html(begin.secondsTo("hh:mm:ss.ms"))
                    );

                    var wrapperElt = $('<div>')
                    .addClass('timecodes')
                    .append(beginAElt);

                    if (end) {
                        var endAElt = $('<a>')
                        .attr('href', '#t=' + end)
                        .on('click', function(event) {
                            event.stopPropagation();
                        });

                        var endTimeElt = $('<time>')
                        .attr('property', 'aa:end')
                        .html(end.secondsTo("hh:mm:ss.ms"));

                        endAElt.append(endTimeElt);

                        wrapperElt
                        .append(endAElt);
                    };


                    $this.prepend(wrapperElt);

                    $this.bind('active', function(event) {
                        console.log('active');
                        //wrapper.scrollTo(this, 2000, {easing: 'easeOutExpo'});
                        wrapper.autoscrollable('scrollto', this);
                    });
                });

                var wrapper = this.$el.find('div.wrapper');
                wrapper.autoscrollable();

            };

            return this;
        },

        toggle: function() {
            //this.$el.contextual('hide');

            if (this.editing) {
                this.model.set({
                    'body': $('textarea', this.$el).val()
                }).save();
            };

            this.editing = !this.editing;
            this.render();
        }
    });


    AA.AnnotationCollectionView = Backbone.View.extend({
        collection: new AA.AnnotationCollection({resource: AA.routes.resourceDetail}),
        el: '#canvas',
        initialize: function() {
            var that = this;

            this.$el
            .on('click', function(event) {
                if (AA.selected) {
                    $(AA.selected).removeClass('selected');
                    AA.selected = undefined;

                    event.stopImmediatePropagation();
                };
            })
            .contextual({
                iconSize: 40,
                iconSpacing: 5,
                onShow: function() {
                    if (AA.current && AA.current !== this) {
                        AA.current.hide();
                    };

                    AA.current = this;
                }
            });

            (function createBtnNewAnnotation() {
                var btn = $('<div>')
                .attr({
                    title: 'new annotation',
                    draggable: false,
                    class: 'icon icon5'

                })
                .on('click', function(event) {
                    var offsetBtn = $(event.currentTarget).position();
                    var offsetCanvas = that.$el.position();
                    var top = offsetBtn.top - offsetCanvas.top;
                    var left = offsetBtn.left - offsetCanvas.left;
                    that.collection.create({top: top, left: left});
                    that.$el.contextual('hide');

                    return false;
                });

                that.$el.contextual('register', 'click', 'cursor', btn);
            })();

            (function createBtnTogglegrid() {
                var btn2 = $('<div>')
                .attr({
                    title: 'toggle grid',
                    draggable: false,
                    class: 'icon icon2'

                })
                .on('click', function(event) {
                    return false;
                });

                that.$el.contextual('register', 'click', 'cursor', btn2);
            })();

            (function createBtnChangeGrid() {
                var btn3 = $('<div>')
                .attr({
                    title: 'change grid',
                    draggable: false,
                    class: 'icon icon3'

                })
                .on('click', function(event) {
                    return false;
                });

                that.$el.contextual('register', 'click', 'cursor', btn3);
            })();

            (function createBtnOrganize() {
                var btn3 = $('<div>')
                .attr({
                    title: 'organize annotation',
                    draggable: false,
                    class: 'icon icon1'

                })
                .on('click', function(event) {
                    that.collection.each(function(model, index) {
                        model.set({
                            'left': 20 + (index * 20),
                            'top': 20 + (index * 20),
                        }, {animate: true}).save();
                    });

                    return false;
                });

                that.$el.contextual('register', 'click', 'cursor', btn3);
            })();

            this.collection.fetch({
                data : {
                    // filters the annotation list for the current Resource at
                    // the API level
                    "resource" : AA.routes.resourceId                  
                },
                success: function(result) {
                    that.render();
                }
            });

            this.listenTo(this.collection, 'add', this.renderOne);
        },
        renderOne: function(model, collection) {
            var $el = this.$el;
            var annotationView = new AA.AnnotationView({model: model});
            $el.append(annotationView.el);

            return this;
        },
        render: function() {
            var $el = this.$el;
            $el.empty();
            this.collection.each(function(annotation) {
                var annotationView = new AA.AnnotationView({model: annotation});
                $el.append(annotationView.el);
            });

            return this;
        }
    });


    AA.Router = Backbone.Router.extend({
        routes: {
            "t=:time": "timechange"
        }
    });
})();


$(function() {
    AA.annotationCollectionView = new AA.AnnotationCollectionView();

    AA.router = new AA.Router();

    var mediaElt = $('#resource').get(0);

    $('#resource').on('canplaythrough', function(event) {
        AA.router.on('route:timechange', function(time) {
            mediaElt.currentTime = parseFloat(time);
        })

        // Start Backbone history a necessary step for bookmarkable URL's
        Backbone.history.start();

        $(document).bind('keydown', "Ctrl+Shift+up", function toggle() {
            if (mediaElt.paused === false) {
                mediaElt.pause();
                AA.router.navigate('t=' + mediaElt.currentTime + 's', {trigger: false, replace: true})
            } else {
                mediaElt.play();
            }
            return false;
        });

        $(document).bind('keydown', "Ctrl+Shift+left", function rewind() {
            mediaElt.currentTime = mediaElt.currentTime - 5;
            AA.router.navigate('t=' + mediaElt.currentTime + 's', {trigger: false, replace: true})
            return false;
        });

        $(document).bind('keydown', "Ctrl+Shift+right", function fastForward() {
            mediaElt.currentTime = mediaElt.currentTime + 5;
            AA.router.navigate('t=' + mediaElt.currentTime + 's', {trigger: false, replace: true})
            return false;
        });
    });
});

// vim: set foldmethod=indent :
