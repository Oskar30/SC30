import pytest
from django.contrib.auth.models import User
from workshop import models


@pytest.fixture
def fix_user():
   user = User.objects.create_user('fix_user', 'test@test.ru', 'test')
   return user

@pytest.fixture
def fix_order(fix_user):
    order = models.Order(person = 'fix_order', contact=12345678900, author=fix_user)
    order.save()
    return order

@pytest.fixture
def fix_expenses(fix_user):
    expenses = models.Expenses(expenses='test_expenses', author=fix_user)
    expenses.save()
    return expenses

@pytest.fixture
def fix_spare(fix_user):
    spare = models.Spare(title='test_spare', author=fix_user)
    spare.save()
    return spare


    
####################

@pytest.mark.django_db
def test_creat_user():
    user = User.objects.create_user('test', 'test@test.ru', 'test')
    assert user

@pytest.mark.django_db
def test_del_user(fix_user):
    fix_user.delete()
    assert User.objects.all().count() == 0


@pytest.mark.django_db
def test_add_order(fix_user):
    order = models.Order(person = 'test', author=fix_user)
    order.save()
    assert order

@pytest.mark.django_db
def test_updete_order(fix_order):
    fix_order.person = 'upd'
    assert fix_order.person == 'upd'

@pytest.mark.django_db
def test_del_order(fix_order):
    fix_order.delete()
    assert models.Order.objects.all().count() == 0


@pytest.mark.django_db
def test_add_expenses(fix_user):
    expenses = models.Expenses(expenses='test_expenses', author=fix_user)
    expenses.save()
    assert expenses

@pytest.mark.django_db
def test_updete_expenses(fix_expenses):
    fix_expenses.expenses = 'upd_expenses'
    assert fix_expenses.expenses == 'upd_expenses'

@pytest.mark.django_db
def test_del_expenses(fix_expenses):
    fix_expenses.delete()
    assert models.Expenses.objects.all().count() == 0


@pytest.mark.django_db
def test_add_spare(fix_user):
    spare = models.Spare(title='test_spare', author=fix_user)
    spare.save()
    assert spare

@pytest.mark.django_db
def test_updete_spare(fix_spare):
    fix_expenses.title = 'upd_title'
    assert fix_expenses.title == 'upd_title'

@pytest.mark.django_db
def test_del_spare(fix_spare):
    fix_spare.delete()
    assert models.Spare.objects.all().count() == 0