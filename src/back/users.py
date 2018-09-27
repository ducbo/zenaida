
from back.models.account import Account


def is_exist(email):
    """
    Return `True` if domain exists, doing query in Domain table.
    """
    return bool(Account.objects.filter(email=email).first())


def find_account(email):
    """
    Return `Account` object created for that email address.
    """
    return Account.objects.filter(email=email).first()


def create_account(email, account_password=None, **kwargs):
    """
    Creates a new user account with given email.
    """
    return Account.objects.create_user(email, password=account_password, **kwargs)