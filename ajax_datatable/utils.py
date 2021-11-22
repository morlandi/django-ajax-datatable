import pprint
import datetime
from django.utils import timezone
from django.conf import settings
from django.utils import formats

import pytz

# Check if sqlparse is available for indentation
try:
    import sqlparse
except ImportError:
    class sqlparse:
        @staticmethod
        def format(text, *args, **kwargs):
            return text

# Check if termcolor is available for coloring
try:
    import termcolor
except ImportError:
    termcolor = None


# Check if Pygments is available for coloring
try:
    import pygments
    from pygments.lexers import SqlLexer
    from pygments.formatters import TerminalTrueColorFormatter
except ImportError:
    pygments = None


# def trace(message, prompt=''):
#     print('\n\x1b[1;36;40m', end='')
#     if prompt:
#         print(prompt + ':')
#     pprint.pprint(message)
#     print('\x1b[0m\n', end='')

# def prettyprint_queryset(qs):
#     print('\x1b[1;33;40m', end='')
#     # https://code.djangoproject.com/ticket/22973 !!!
#     try:
#         message = sqlparse.format(str(qs.query), reindent=True, keyword_case='upper')
#     except Exception as e:
#         message = str(e)
#         if not message:
#             message = repr(e)
#         message = 'ERROR: ' + message
#     print(message)
#     print('\x1b[0m\n')


def trace(message, color='cyan', on_color=None, attrs=None, prompt='', prettify=False):

    if prettify:
        text = pprint.pformat(message)
    else:
        text = str(message)

    if prompt:
        text = '=== ' + prompt + ': \n' + text

    if termcolor and (color or on_color):
        termcolor.cprint(text, color=color, on_color=on_color, attrs=attrs)
    else:
        print(text)


def prettyprint_query(query, colorize=True, prettify=True):

    def _str_query(sql):
        # Borrowed by morlandi from sant527
        # See: https://github.com/bradmontgomery/django-querycount/issues/22
        if prettify:
            sql = sqlparse.format(sql, reindent=True)
        if colorize and pygments:
            # Highlight the SQL query
            sql = pygments.highlight(
                sql,
                SqlLexer(),
                TerminalTrueColorFormatter(style='monokai')
                # TerminalTrueColorFormatter()
            )
        return sql

    sql = _str_query(query)
    print(sql)


def prettyprint_queryset(qs, colorize=True, prettify=True):
    prettyprint_query(str(qs.query), colorize=colorize, prettify=prettify)


def format_datetime(dt, include_time=True):
    """
    Here we adopt the following rule:
    1) format date according to active localization
    2) append time in military format
    """
    if dt is None:
        return ''

    if isinstance(dt, datetime.datetime):
        try:
            dt = timezone.localtime(dt)
        except Exception:
            local_tz = pytz.timezone(getattr(settings, 'TIME_ZONE', 'UTC'))
            dt = local_tz.localize(dt)
    else:
        assert isinstance(dt, datetime.date)
        include_time = False

    use_l10n = getattr(settings, 'USE_L10N', False)
    text = formats.date_format(dt, use_l10n=use_l10n, format='SHORT_DATE_FORMAT')
    if include_time:
        text += dt.strftime(' %H:%M:%S')
    return text


def parse_date(formatted_date):
    parsed_date = None
    for date_format in formats.get_format('DATE_INPUT_FORMATS'):
        try:
            parsed_date = datetime.datetime.strptime(formatted_date, date_format)
        except ValueError:
            continue
        else:
            break
    if not parsed_date:
        raise ValueError
    return parsed_date.date()
