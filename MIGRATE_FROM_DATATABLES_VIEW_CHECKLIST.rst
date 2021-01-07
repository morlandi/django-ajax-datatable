Howto migrate your Django project from django-datatables-view to django-ajax-datatable
--------------------------------------------------------------------------------------

- in your setting's INSTALLED_APPS, replace `datatables_view` with `ajax_datatable`
- in your settings, replace `DATATABLES_VIEW_*` with `AJAX_DATATABLE_*`
- in your Python imports, replace `from datatables_view` with `from ajax_datatable`
- in your templates, replace `datatables_view` with `ajax_datatable`
- in your templates, replace **folder** `datatables_view` with **folder** `ajax_datatable`
- in your templates, replace `datatables_view_tags` with `ajax_datatable_tags`
- in your templates, replace `DatatablesViewUtils` with `AjaxDatatableViewUtils`
- in your templates, if you included `datatables_view/js/datatables_utils.js`, include `ajax_datatable/js/utils.js` instead
- in your derived view classes, replace the base class from `DatatablesView` to `AjaxDatatableView`

Since v4.1.0, these settings:

- AJAX_DATATABLE_ENABLE_QUERYDICT_TRACING
- AJAX_DATATABLE_ENABLE_QUERYSET_TRACING

have been replaced by:

- AJAX_DATATABLE_TRACE_COLUMNDEFS
- AJAX_DATATABLE_TRACE_QUERYDICT
- AJAX_DATATABLE_TRACE_QUERYSET
