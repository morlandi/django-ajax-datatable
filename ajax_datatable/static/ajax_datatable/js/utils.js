'use strict';

window.AjaxDatatableViewUtils = (function() {

    //var _search_icon_html = '<div style="border: 1px solid #ccc; text-align: center;">?</div>';
    var _options = {};

    var _html_daterange_widget =
        'From: <input type="date" id="date_from" class="datepicker">' +
        'To: <input type="date" id="date_to" class="datepicker">';


    function init(options) {
        /*
            Example:

            AjaxDatatableViewUtils.init({
                search_icon_html: '<i class="fa fa-search"></i>',
                language: {
                },
                fn_daterange_widget_initialize: function(table, data) {
                    var wrapper = table.closest('.dataTables_wrapper');
                    var toolbar = wrapper.find(".toolbar");
                    toolbar.html(
                        '<div class="daterange" style="float: left; margin-right: 6px;">' +
                        '{% trans "From" %}: <input type="text" class="date_from" autocomplete="off">' +
                        '&nbsp;&nbsp;' +
                        '{% trans "To" %}: <input type="text" class="date_to" autocomplete="off">' +
                        '</div>'
                    );
                    var date_pickers = toolbar.find('.date_from, .date_to');
                    date_pickers.datepicker();
                    date_pickers.on('change', function(event) {
                        // Annotate table with values retrieved from date widgets
                        var dt_from = toolbar.find('.date_from').data("datepicker");
                        var dt_to = toolbar.find('.date_to').data("datepicker");
                        table.data('date_from', dt_from ? dt_from.getFormattedDate("yyyy-mm-dd") : '');
                        table.data('date_to', dt_to ? dt_to.getFormattedDate("yyyy-mm-dd") : '');
                        // Redraw table
                        table.api().draw();
                    });
                }
            });


            then:

                <div class="table-responsive">
                    <table id="datatable" width="100%" class="table table-striped table-bordered dataTables-log">
                    </table>
                </div>

                <script language="javascript">
                    $(document).ready(function() {

                        // Subscribe "rowCallback" event
                        $('#datatable').on('rowCallback', function(event, table, row, data ) {
                            //$(e.target).show();
                            console.log('rowCallback(): table=%o', table);
                            console.log('rowCallback(): row=%o', row);
                            console.log('rowCallback(): data=%o', data);
                        }

                        // Initialize table
                        AjaxDatatableViewUtils.initialize_table(
                            $('#datatable'),
                            "{% url 'frontend:object-datatable' model|app_label model|model_name %}"
                        );
                    });
                </script>

        */
        _options = options;

        if (!('language' in _options)) {
            _options.language = {};
        }
    }


    function _handle_column_filter(table, data, target) {
        var index = target.data('index');
        var value = target.val();

        var column = table.api().column(index);
        var old_value = column.search();
        console.log('Request to search value %o in column %o (current value: %o)', value, index, old_value);
        if (value != old_value) {
            console.log('searching ...');
            column.search(value).draw();
        }
        else {
            console.log('skipped');
        }
    };

    /*
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if(c.indexOf(name) == 0)
            return c.substring(name.length,c.length);
        }
        return "";
    }
    */

    function getCookie(name) {
        var cookieValue = null;
        var value = '; ' + document.cookie,
            parts = value.split('; ' + name + '=');
        if (parts.length == 2) cookieValue = parts.pop().split(';').shift();
        return cookieValue;
    }

    function getCSRFToken() {
        var csrftoken = getCookie('csrftoken');
        if (csrftoken == null) {
            csrftoken = $('input[name=csrfmiddlewaretoken]').val();
        }
        return csrftoken;
    }

    function _setup_column_filters(table, data) {

        if (data.show_column_filters) {

            var filter_row = '<tr class="datatable-column-filter-row">';
            $.each(data.columns, function(index, item) {
                if (item.visible) {
                    if (item.searchable) {
                        var html = '';
                        if ('choices' in item && item.choices) {

                            // See: https://www.datatables.net/examples/api/multi_filter_select.html
                            var select = $('<select data-index="' + index.toString() + '"><option value=""></option></select>');
                            $(item.choices).each(function(index, choice) {
                                var option = $("<option>").attr('value', choice[0]).text(choice[1]);
                                if (choice[0] === item.initialSearchValue) {
                                    option.attr('selected', 'selected');
                                }
                                select.append(option);
                            });
                            html = $('<div>').append(select).html();
                        }
                        else {
                            var input = $('<input>')
                                .attr('type', 'text')
                                .attr('data-index', index)
                                .attr('placeholder', '...')
                                .attr('value', item.initialSearchValue ? item.initialSearchValue : '')
                            html = $('<div>').append(input).html();
                        }
                        if (item.className) {
                            filter_row += '<th class="' + item.className + '">' + html + '</th>';
                        }
                        else {
                            filter_row += '<th>' + html + '</th>';
                        }
                    }
                    else {
                        if (index == 0) {
                            // var search_icon_html = _options.search_icon_html === undefined ?
                            //     '<div style="border: 1px solid #ccc; text-align: center;">&nbsp;</div>' : _options.search_icon_html;
                            var search_icon_html = _options.search_icon_html === undefined ? '' : _options.search_icon_html;
                            //filter_row += '<th><i class="fa fa-search"></i>&nbsp;</th>';
                            filter_row += '<th>' + search_icon_html + '</th>';
                        }
                        else {
                            filter_row += '<th></i>&nbsp;</th>';
                        }
                    }
                }
            });
            filter_row += '</tr>';

            var wrapper = table.closest('.dataTables_wrapper');
            $(filter_row).appendTo(
                wrapper.find('thead')
            );

            var column_filter_row = wrapper.find('.datatable-column-filter-row')
            column_filter_row.find('input,select').off().on('keyup change', function(event) {
                var target = $(event.target);
                _handle_column_filter(table, data, target);
            });

            /*
            // Here, we could explicitly invoke the handler for each column filter,
            // to make sure that the initial table contents respect any (possible)
            // default value assigned to column filters.
            // This works, but causes multiple POST requests during the first table rendering.

            column_filter_row.find('input,select').each( function(index, item) {
                var target = $(item);
                _handle_column_filter(table, data, target);
            });

            So we now prefer to supply the initial search value in the column initialization:
            see "searchCols" table attribute, as documented here:
            https://datatables.net/reference/option/searchCols
            */
        }
    };


    function _bind_row_tools(table, url, options, extra_data)
    {
        //console.log('*** _bind_row_tools()');

        if (options.full_row_select) {

            // Full row select: when user clicks anywhere in the row,
            // expand it to show further details
            table.api().on('click', 'td', function(event) {
                //event.preventDefault();
                var tr = $(this).closest('tr');

                // Dont' close child when clicking inside child itself,
                // unless clicking on a button with class "btn-close"
                if (tr.hasClass('details') && !$(event.target).hasClass('btn-close')) {
                    return;
                }

                var row = table.api().row(tr);
                if (row.child.isShown()) {
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    table.find('tr').removeClass('shown');
                    table.api().rows().every(function( rowIdx, tableLoop, rowLoop) {
                        this.child.hide();
                    });
                    if (!tr.hasClass('details')) {
                        row.child(_load_row_details(row.data(), url, extra_data), 'details').show('slow');
                        tr.addClass('shown');
                    }
                }
            });

        } else {

            // Use "plus" and "minus" links to toggle row details
            table.api().on('click', 'td.dataTables_row-tools .plus, td.dataTables_row-tools .minus', function(event) {
                event.preventDefault();
                var tr = $(this).closest('tr');
                var row = table.api().row(tr);
                if (row.child.isShown()) {
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    //row.child(_load_row_details(row.data(), url), 'details').show('slow');
                    //tr.addClass('shown');
                    var data = _load_row_details(row.data(), url, extra_data);
                    if (options.detail_callback) {
                        options.detail_callback(data, tr);
                    }
                    else {
                        row.child(data, 'details').show('slow');
                    }
                    tr.addClass('shown');
                }
            });
        }
    };

    function _load_row_details(rowData, url, extra_data) {

        var div = $('<div/>')
            .addClass('row-details-wrapper loading')
            .text('Loading...');

        if (rowData !== undefined) {

            var data = {
                action: 'details',
                pk: rowData['pk']
            };
            if (extra_data) {
                Object.assign(data, extra_data);
            }

            $.ajax({
                url: url,
                // data: {
                //     action: 'details',
                //     pk: rowData['pk']
                // },
                data: data,
                dataType: 'json',
                success: function(json) {
                    var parent_row_id = json['parent-row-id'];
                    if (parent_row_id !== undefined) {
                        div.attr('data-parent-row-id', parent_row_id);
                    }
                    div.html(json.html).removeClass('loading');
                }
            });
        }

        return div;
    };


    function adjust_table_columns() {
        // Adjust the column widths of all visible tables
        // https://datatables.net/reference/api/%24.fn.dataTable.tables()
        $.fn.dataTable
            .tables({
                visible: true,
                api: true
            })
            .columns.adjust();
    };


    function _daterange_widget_initialize(table, data) {
        if (data.show_date_filters) {
            if (_options.fn_daterange_widget_initialize) {
                _options.fn_daterange_widget_initialize(table, data);
            }
            else {
                var wrapper = table.closest('.dataTables_wrapper');
                var toolbar = wrapper.find(".toolbar");
                toolbar.html(
                    '<div class="daterange" style="float: left; margin-right: 6px;">' +
                    '<span class="from"><label>From</label>: <input type="date" class="date_from datepicker"></span>' +
                    '<span class="to"><label>To</label>: <input type="date" class="date_to datepicker"></span>' +
                    '</div>'
                );
                toolbar.find('.date_from, .date_to').on('change', function(event) {
                    // Annotate table with values retrieved from date widgets
                    table.data('date_from', wrapper.find('.date_from').val());
                    table.data('date_to', wrapper.find('.date_to').val());
                    // Redraw table
                    table.api().draw();
                });
            }
        }
    }


    function after_table_initialization(table, data, url, options, extra_data) {
        //console.log('*** after_table_initialization()');
        _bind_row_tools(table, url, options, extra_data);
        _setup_column_filters(table, data);
    }


    function _write_footer(table, html) {
        var wrapper = table.closest('.dataTables_wrapper');
        var footer = wrapper.find('.dataTables_extraFooter');
        if (footer.length <= 0) {
            $('<div class="dataTables_extraFooter"></div>').appendTo(wrapper);
            footer = wrapper.find('.dataTables_extraFooter');
        }
        footer.html(html);
    }

    function initialize_table(element, url, extra_options={}, extra_data={}) {

        var data = {action: 'initialize'};
        if (extra_data) {
            Object.assign(data, extra_data);
        }
        $.ajax({
            type: 'POST',
            //url: url + '?action=initialize',
            url: url,
            data: data,
            dataType: 'json',
            headers: {'X-CSRFToken': getCSRFToken()}
        }).done(function(data, textStatus, jqXHR) {

            // https://datatables.net/manual/api#Accessing-the-API
            // It is important to note the difference between:
            //    - $(selector).DataTable(): returns a DataTables API instance
            //    - $(selector).dataTable(): returns a jQuery object
            // An api() method is added to the jQuery object so you can easily access the API,
            // but the jQuery object can be useful for manipulating the table node,
            // as you would with any other jQuery instance (such as using addClass(), etc.).

            var options = {
                processing: true,
                serverSide: true,
                scrollX: true,
                autoWidth: true,
                dom: '<"toolbar">lrftip',
                language: _options.language,
                full_row_select: false,
                // language: {
                //     "decimal":        "",
                //     "emptyTable":     "Nessun dato disponibile per la tabella",
                //     "info":           "Visualizzate da _START_ a _END_ di _TOTAL_ entries",
                //     "infoEmpty":      "Visualizzate da 0 a 0 di 0 entries",
                //     "infoFiltered":   "(filtered from _MAX_ total entries)",
                //     "infoPostFix":    "",
                //     "thousands":      ",",
                //     "lengthMenu":     "Visualizza _MENU_ righe per pagina",
                //     "loadingRecords": "Caricamento in corso ...",
                //     "processing":     "Elaborazione in corso ...",
                //     "search":         "Cerca:",
                //     "zeroRecords":    "Nessun record trovato",
                //     "paginate": {
                //         "first":      "Prima",
                //         "last":       "Ultima",
                //         "next":       "Prossima",
                //         "previous":   "Precedente"
                //     },
                //     "aria": {
                //         "sortAscending":  ": activate to sort column ascending",
                //         "sortDescending": ": activate to sort column descending"
                //     }
                // },
                ajax: function(data, callback, settings) {
                      var table = $(this);
                      data.date_from = table.data('date_from');
                      data.date_to = table.data('date_to');
                      if (extra_data) {
                          Object.assign(data, extra_data);
                      }
                      console.log("data tx: %o", data);
                      $.ajax({
                          type: 'POST',
                          url: url,
                          data: data,
                          dataType: 'json',
                          cache: false,
                          crossDomain: false,
                          headers: {'X-CSRFToken': getCSRFToken()}
                      }).done(function(data, textStatus, jqXHR) {
                          console.log('data rx: %o', data);
                          callback(data);

                          var footer_message = data.footer_message;
                          if (footer_message !== null) {
                              _write_footer(table, footer_message);
                          }

                      }).fail(function(jqXHR, textStatus, errorThrown) {
                          console.log('ERROR: ' + jqXHR.responseText);
                      });
                },
                columns: data.columns,
                searchCols: data.searchCols,
                lengthMenu: data.length_menu,
                order: data.order,
                initComplete: function() {
                    // HACK: wait 200 ms then adjust the column widths
                    // of all visible tables
                    setTimeout(function() {
                        AjaxDatatableViewUtils.adjust_table_columns();
                    }, 200);

                    // Notify subscribers
                    //console.log('Broadcast initComplete()');
                    table.trigger(
                        'initComplete', [table]
                    );
                },
                drawCallback: function(settings) {
                    // Notify subscribers
                    //console.log('Broadcast drawCallback()');
                    table.trigger(
                        'drawCallback', [table, settings]
                    );
                },
                rowCallback: function(row, data) {
                    // Notify subscribers
                    //console.log('Broadcast rowCallback()');
                    table.trigger(
                        'rowCallback', [table, row, data]
                    );
                },
                footerCallback: function (row, data, start, end, display) {
                    // Notify subscribers
                    //console.log('Broadcast footerCallback()');
                    table.trigger(
                        'footerCallback', [table, row, data, start, end, display]
                    );
                }
            }

            if (extra_options) {
                Object.assign(options, extra_options);
            }

            var table = element.dataTable(options);

            _daterange_widget_initialize(table, data);
            after_table_initialization(table, data, url, options, extra_data);
        })
    }


    function redraw_all_tables() {
        $.fn.dataTable.tables({
            api: true
        }).draw();
    }


    // Redraw table holding the current paging position
    function redraw_table(element) {
        var table = $(element).closest('table.dataTable');
        // console.log('element: %o', element);
        // console.log('table: %o', table);
        table.DataTable().ajax.reload(null, false);
    }


    return {
        init: init,
        initialize_table: initialize_table,
        adjust_table_columns: adjust_table_columns,
        redraw_all_tables: redraw_all_tables,
        redraw_table: redraw_table
    };

})();
