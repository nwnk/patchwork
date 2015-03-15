var pw = (function() {
    var _this,
        exports = {},
        ctx = {
            project: null,
            series: null
        };

    function get_cookie(name) {
        var value = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    value = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return value;
    }

    var columnsMap = {
        'Series': 'name',
        'Patches': 'n_patches',
        'Submitter': 'submitter__name',
        'Reviewer': 'reviewer__name',
        'Submitted': 'submitted',
        'Updated': 'last_updated'
    };

    function series_writer(record) {
        return '<a href="/series/' + record['id'] + '/">' + record[this.id] + '</a>';
    }

    function date_writer(record) {
        return record[this.id].substr(0, 10);
    }

    function reviewer_writer(record) {
        reviewer = record[this.id];
        if (!reviewer)
            return '<em class="text-muted">None</span>';
        else
            return reviewer;
    }

    exports.amend_context = function(new_ctx) {
        $.extend(ctx, new_ctx);
    }

    exports.init = function(init_ctx) {
        _this = this;

        this.amend_context(init_ctx);

        ctx.csrftoken = get_cookie('csrftoken');

        $.dynatableSetup({
            dataset: {
                perPageDefault: 20,
                perPageOptions: [20, 50, 100]
            },
            params: {
                perPage: 'perpage',
                records: 'results',
                queryRecordCount: 'count',
                totalRecordCount: 'count',
                sorts: 'ordering'
            },
            inputs: {
                pageText: '',
                paginationPrev: '« Previous',
                paginationNext: 'Next »',
                paginationGap: [1,1,1,1],
            },
            writers: {
                'name': series_writer,
                'submitted': date_writer,
                'last_updated': date_writer,
                'reviewer__name': reviewer_writer
            }
        });
    }

    exports.setup_series_list = function(selector, url) {
        var table = $(selector);
        var url;

        if (typeof url == 'undefined')
            url = '/api/1.0/projects/' + ctx.project + '/series/';

        table.bind('dynatable:preinit', function(e, dynatable) {
            dynatable.utility.textTransform.PatchworkSeries = function(text) {
                return columnsMap[text];
            };
        }).dynatable({
            features: {
                search: false,
                recordCount: false,
            },
            table: {
                defaultColumnIdStyle: 'PatchworkSeries',
            },
            dataset: {
                ajax: true,
                ajaxUrl: url,
                ajaxOnLoad: true,
                records: []
            }
        });

        table.stickyTableHeaders();
    }

    exports.setup_series = function(config) {
        var column_num, column_name;

        column_num = $('#' + config.patches + ' tbody tr td:first-child');
        column_name = $('#' + config.patches + ' tbody tr td:nth-child(2) a');

        for (i = 0; i < column_num.length; i++) {
            var name = $(column_name[i]).html();
            var s = name.split(']');

            if (s.length == 1) {
                $(column_num[i]).html('1');
            } else {
                var matches = s[0].match(/(\d+)\/(\d+)/);

                $(column_name[i]).html(s.slice(1).join(']'));

                if (!matches) {
                    $(column_num[i]).html('1');
                    continue;
                }

                $(column_num[i]).html(matches[1]);
            }
        }
    }

    function setup_autocompletion(field) {
        var $s = $('#edit-' + field.name + ' input');
        var s = $s[0].selectize;

        if (!field.autocomplete)
            return;

        if (s)
            return;

        $s.selectize({
            valueField: 'pk',
            labelField: field.autocomplete.display_field,
            searchField: field.autocomplete.search_fields,
            maxItems: 1,
            persist: false,
            openOnFocus: false,
            render: {
                option: field.autocomplete.render || function(item, escape) {
                        return '<div>' + escape(item[field.autocomplete.display_field]) + '</div>';
                },
                item: field.autocomplete.render || function(item, escape) {
                        return '<div>' + escape(item[field.autocomplete.display_field]) + '</div>';
                }
            },
            load: function(query, callback) {
                if (query.length < 3)
                    return callback();

                req = $.ajax({
                    url: field.autocomplete.url + '/?q=' + encodeURIComponent(query) + '&l=10',
                    error: function() {
                        callback();
                    },
                    success: function(res) {
                        callback(res);
                    }
                });
            }
        });

        s = $s[0].selectize;
        s.on('item_add', function(value) {
            $('#save-' + field.name).removeClass('disabled');
        });

        s.on('item_remove', function(value) {
            $('#save-' + field.name).removeClass('disabled');
        });

    }

    function cleanup_autocompletion(field) {
        var $s = $('#edit-' + field.name + ' input');
        var s = $s[0].selectize;

        s.destroy();
        delete $s[0].selectize;
    }

    function field_setup(field) {
        /* what to do when the edit icon is clicked */
        $('#field-' + field.name + ' .glyphicon-pencil').click(function() {
            var input = $('#edit-' + field.name + ' input');

            $(this).parent().hide();
            $('#save-' + field.name).addClass('disabled');
            $('#edit-' + field.name).show();

            setup_autocompletion(field);

            if (field.value) {
                input[0].selectize.addOption(field.value);
                input[0].selectize.setValue(field.value.pk);
            }
            input[0].selectize.focus();
        });

        function field_refresh(field) {
            var content;

            if (field.is_null())
                content = '<em class="text-muted">None</em>';
            else
                content = field.text();

            $('#field-' + field.name + '-text').html(content);
        }

        /* the save button is clicked */
        $('#save-' + field.name).click(function() {
            var $s = $('#edit-' + field.name + ' input');
            var s = $s[0].selectize;
            var val = parseInt(s.getValue()) || null;
            var patch_data = {};

            patch_data[field.name] = val;

            $.ajax({
                url: '/api/1.0/series/' + ctx.series + '/',
                headers: {
                    'X-HTTP-Method-Override': 'PATCH',
                    'X-CSRFToken': ctx.csrftoken
                },
                type: 'POST',
                data: patch_data,
                success: function(response) {
                    field.init_from_series(response);
                    field_refresh(field);
                    $('#edit-' + field.name).hide();
                    $('#field-' + field.name).show();
                },
                /* TODO: show the error to the user, maybe use the 'details'
                 * from the response */
                error: function(ctx, status, error) {
                    console.log("Couldn't save " + field.name + ": " + status, error);
                }
            })
        });

        /* the cancel button is clicked */
        $('#cancel-' + field.name).click(function() {
            $('#edit-' + field.name).hide();
            $('#field-' + field.name).show();
        });

    }

    exports.setup_editable_fields = function(fields) {
        fields.forEach(field_setup);
    }

    return exports
}());
