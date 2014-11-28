var pw = (function() {
    var _this,
        exports = {},
        ctx = {
            project: null
        };

    var columnsMap = {
        'Series': 'name',
        'Patches': 'n_patches',
        'Submitter': 'submitter_name',
        'Reviewer': 'reviewer_name',
        'Submitted': 'submitted',
        'Updated': 'last_updated'
    };

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

    exports.init = function(init_ctx) {
        _this = this;

        $.extend(ctx, init_ctx);

        $.dynatableSetup({
            dataset: {
                perPageDefault: 20,
                perPageOptions: [20, 50, 100]
            },
            params: {
                perPage: 'perpage',
                records: 'results',
                queryRecordCount: 'count',
                totalRecordCount: 'count'
            },
            inputs: {
                pageText: '',
                paginationPrev: '« Previous',
                paginationNext: 'Next »',
                paginationGap: [1,1,1,1],
            },
            writers: {
                'submitted': date_writer,
                'last_updated': date_writer,
                'reviewer_name': reviewer_writer
            }
        });
    }

    exports.setup_series_list = function(selector) {
        var table = $(selector);

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
                ajaxUrl: '/api/1.0/projects/' + ctx.project + '/series/',
                ajaxOnLoad: true,
                records: []
            }
        });

        table.stickyTableHeaders();
    }

    return exports
}());
