Howto migrate your Django project from django-datatables-view to django-ajax-datatable
--------------------------------------------------------------------------------------

- in your settings INSTALLED_APPS, replace `datatables_view` with `ajax_datatable`
- in your Python imports, replace `from datatables_view` with `from ajax_datatable`
- in your templates, replace `datatables_view` with `ajax_datatable`
- in your templates, replace `DatatablesViewUtils` with `AjaxDatatableViewUtils`
- in your derived view classes, replace the base class from `DatatablesView` to `AjaxDatatableView`
