from unittest.mock import patch
from schemas.game import GameCreate, GameResponse
from services.game import create_game, read_game, update_game, delete_game
from models.game import Game
from pytest import raises

def refresh(obj):
    obj.id = 1

@patch('services.game.Session')
def test_create_game(mock_session):
    mock_session.return_value.__enter__.return_value.refresh.side_effect = refresh
    new_game = GameCreate(name='Action Game', description='fast paced',
                          tag='ACTION', platform='xbox')
    
    result = create_game(new_game)
    assert result.name == 'Action Game'

@patch('services.game.Session')
def test_read_game(mock_session):
    game = Game(id=1, name='Action Game', description='fast paced', tag='ACTION', platform='xbox')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = game
    result = read_game(1)
    assert result.name == 'Action Game'

@patch('services.game.Session')
def test_update_game(mock_session):
    game = Game(id=1, name='Action Game', description='fast paced', tag='ACTION', platform='xbox')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = game
    result = update_game(GameResponse(id=1, name='New Name', description='fast paced', tag='ACTION', platform='xbox'))
    assert result.name == 'New Name' 

@patch('services.game.Session')
def test_delete_game(mock_session):
    game = Game(id=1, name='Action Game', description='fast paced', tag='ACTION', platform='xbox')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = game
    result = delete_game(1)
    assert result == True

@patch('services.game.Session')
def test_failed_read_game(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = read_game(1)

@patch('services.game.Session')
def test_failed_update_game(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = update_game(GameResponse(id=1, name='New Name', description='fast paced', tag='ACTION', platform='xbox'))
        
@patch('services.game.Session')
def test_failed_delete_game(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = delete_game(1)
