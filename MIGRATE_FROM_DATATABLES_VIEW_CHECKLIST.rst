Howto migrate your Django project from django-datatables-view to django-ajax-datatable
--------------------------------------------------------------------------------------

- in your setting's INSTALLED_APPS, replace `datatables_view` with `ajax_datatable`
- in your settings, replace `DATATABLES_VIEW_*` with `AJAX_DATATABLE_*`
- in your Python imports, replace `from datatables_view` with `from ajax_datatable`
- in your templates, replace `datatables_view` with `ajax_datatable`
- in your templates, replace `DatatablesViewUtils` with `AjaxDatatableViewUtils`
- in yout templates, if you included `datatables_view/js/datatables_utils.js`, include `ajax_datatable/js/utils.js` instead
- in your derived view classes, replace the base class from `DatatablesView` to `AjaxDatatableView`
