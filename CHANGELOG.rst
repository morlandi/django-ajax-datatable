.. :changelog:

History
=======

v4.0.1
------
* A few typo fixes here and there

v4.0.0
------
* package renamed from `django-datatables-view` to `django-ajax-datatable`
* published on PyPI
* example project added
* setup of demo site `http://django-ajax-datatable-demo.brainstorm.it`

v3.2.3
------
* "data-parent-row-id" attribute added to details row

v3.2.2
------
* accept positions expressed as column names in initial_order[]

v3.2.1
------
* add className to filters
* improved filtering with choices by including foreign_fields
* optional "boolean" column attribute to treat calculated column as booleans on explicit request
* optional "max_length" column attribute to clip results

v3.2.0
------
* Automatic addition of table row ID (see `get_table_row_id()`)
* `request` parameter added to `prepare_results()` and `get_response_dict()`

v3.1.4
------
* fix checkbox and radio buttons not working in a form embedded in the details row when full_row_select is active

v3.1.3
------
* Better behaviour for full_row_select

v3.1.2
------
* `initialSearchValue` can now be a value or a callable object

v3.1.1
------
* Silly JS fix

v3.1.0
------
* choices / autofilter support for column filters
* optional *initialSearchValue* for column filters
* **Backward incompatible change**: any unrecognized column_defs attribute will raises an exception

v3.0.4
------
* Support length_menu = -1 (which means: "all")

v3.0.3
------
* Use `full_row_select=true` to toggled row details by clicking anywhere in the row

v3.0.2
------
* Sanity check for initial_order[]

v3.0.1
------
* js fix (same as v2.3.5)

v3.0.0
------
* Bump major version to welcome Django 3

v2.3.5
------
* js fix

v2.3.4
------
* Add support for Django 3.0, drop Python 2

v.2.3.3
-------
* Some JS utilities added

v2.3.2
------
* improved queryset optimization

v2.3.1
------
* fix queryset optimization

v2.3.0
------
* queryset optimization

v2.2.9
------
* optional extra_data dictionary accepted by initialize_table()

v2.2.8
------
* Remove `table-layout: fixed;` style from HTML table, as this causes problems in the columns' widths computation

v2.2.7
------
* Explicitly set width of "row tools" column
* Localize "search" prompt in column filters

v2.2.6
------
* Experimental: Optionally control the (minimum) width of each single column

v2.2.5
------
* cleanup

v2.2.4
------
* optionally specified extra options to initialize_table()

v2.2.3
------
* accept language options

v2.2.2
------
* fix default footer

v2.2.1
------
* README revised

v2.2.0
------
* Merge into master

v2.1.3
------
* Remove initialize_datatable() from main project and replace with DatatablesViewUtils.initialize_table() to share common behaviour
* Notify Datatable subscribers with various events
* Cleanup global filtering on dates range
* Derived view class can now specify 'latest_by' when different from model.get_latest_by
* Documentation revised

v2.1.2
------
* basic support for DateField and DateTimeField filtering (exact date match)

v2.1.1
------
* choices lookup revised

v2.1.0
------
* `static/datatables_view/js/datatables_utils.js` renamed as `static/datatables_view/js/utils.js`
* js helper encapsulated in DatatablesViewUtils module
* First "almost" working column filtering - good enought for text search

v2.0.6
------
* Accept either GET or POST requests

v2.0.5
------
* Global "get_latest_by" filtering improved

v2.0.4
------
* Filter tracing (for debugging)

v2.0.0
------
* DatatablesView refactoring: columns_specs[] used as a substitute for columns[],searchable_columns[] and foreign_fields[]

v1.2.4
------
* recognize datatime.date column type

v1.2.3
------
* render_row_details() passes model_admin to the context, to permit fieldsets navigation

v1.2.2
------
* generic tables explained
* render_row_details customizable via templates

v1.2.1
------
* merged PR #1 from Thierry BOULOGNE

v1.2.0
------
* Incompatible change: postpone column initialization and pass the request to get_column_defs() for runtime table layout customization

v1.0.1
------
* fix choices lookup

v1.0.0
------
* fix search
* better distribution (make sure templates and statics are included)

v0.0.2
------
* Package version added
