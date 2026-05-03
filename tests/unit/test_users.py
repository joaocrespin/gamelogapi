from unittest.mock import patch
from services.user import create_user, login_user, user_stats
from schemas.user import UserCreate, UserLogin
from models.user import User
from jwt import decode
from pwdlib import PasswordHash
from pytest import raises
from datetime import datetime

password_hash = PasswordHash.recommended()

def refresh(obj):
    obj.id = 1

@patch('services.user.Session')
def test_create_user(mock_session):
    # Sobrescreve o refresh do banco para adicionar um id ao objeto criado
    mock_session.return_value.__enter__.return_value.refresh.side_effect = refresh
    new_user = UserCreate(name='TestName', email='testmail@test.com', password='pass12word4!')
    response = create_user(new_user)
    assert response.name == new_user.name


@patch('services.user.Session')
def test_login_user(mock_session):
    user = User(id=1, name='TestName', email='testmail@test.com', password=password_hash.hash('pass12word4!'))
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = user
    response = login_user(UserLogin(email='testmail@test.com', password='pass12word4!'))
    assert response != False

@patch('services.user.Session')
def test_user_status(mock_session):
    user = User(id=1, name='TestName', email='testmail@test.com', password=password_hash.hash('pass12word4!'), created_at=datetime.now())
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = user
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar.return_value = 1
    response = user_stats('TestName')
    assert response.days_since_creation == 0

@patch('services.user.Session')
def test_failed_login_user(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        response = login_user(UserLogin(email='notauser@test.com', password='pass12word4!'))

@patch('services.user.Session')
def test_failed_user_status(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        user_stats('TestName')