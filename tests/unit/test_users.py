from unittest.mock import patch
from services.user import create_user, login_user
from schemas.user import UserCreate, userLogin, UserResponse
from models.user import User
from jwt import decode
from pwdlib import PasswordHash

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
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = User(id=1, name='TestName', email='testmail@test.com', password=password_hash.hash('pass12word4!'))
    response = login_user(userLogin(email='testmail@test.com', password='pass12word4!'))
    assert response != False


@patch('services.user.Session')
def test_failed_login_user(mock_session):
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
    response = login_user(userLogin(email='notauser@test.com', password='pass12word4!'))
    assert response == False