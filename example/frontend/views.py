from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from backend.models import Track


User = get_user_model()


def tracks_list_view(request):
    """
    Render the page which contains the table.
    That will in turn invoke (via Ajax) object_datatable_view(), to fill the table content
    """
    model = Track
    template_name = "frontend/track/list.html"

    return render(request, template_name, {
        #'model': model,
    })

