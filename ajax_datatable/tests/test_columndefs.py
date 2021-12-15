# from django.test import TestCase
from unittest import TestCase
import factory
import factory.random
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from ajax_datatable import AjaxDatatableView


User = get_user_model()


class UserAjaxDatatableView(AjaxDatatableView):

    model = User

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {
            'name': 'id',
            'visible': False,
        }, {
            'name': 'username',
        }, {
            'name': 'first_name',
        }, {
            'name': 'last_name',
        }
    ]


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    password = 'password'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class TestColumnDefs(TestCase):

    def setUp(self):
        factory.random.reseed_random('test_static_columns')
        self.build_fake_data()

    def tearDown(self):
        User.objects.all().delete()

    def build_fake_data(self):
        UserFactory.create_batch(100)

    def test_static_columns(self):

        view = UserAjaxDatatableView()
        queryset = view.get_initial_queryset()
        per_page = 10
        paginator = Paginator(queryset, per_page=per_page)

        request = None
        view.initialize(request)
        response_dict = view.get_response_dict(request, paginator, draw_idx=0, start_pos=0)

        self.assertEqual(100, response_dict['recordsTotal'])
        self.assertEqual(100, response_dict['recordsFiltered'])
        data = response_dict['data']
        self.assertEqual(per_page, len(data))

        for row in data:
            user = User.objects.get(id=row['pk'])
            self.assertEqual(user.username, row['username'])
            self.assertEqual(user.first_name, row['first_name'])
            self.assertEqual(user.last_name, row['last_name'])
