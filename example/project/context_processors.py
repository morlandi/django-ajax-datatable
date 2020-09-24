import project


def project_settings(request):

    return {
        'PROJECT_BUILD': project.__build__,
    }
