from unittest.mock import patch
from services.library import trending_game
from models.game import Game
from pytest import raises

@patch('services.library.rconn')
def test_trending_cache_hit(mock_rconn):
    mock_rconn.get.return_value = '1'
    result = trending_game()
    assert result == '1'

@patch('services.library.rconn')
@patch('services.library.Session')
def test_trending_cache_miss(mock_session, mock_rconn):
    game = Game(id=1, name='Action Game', description='fast paced', tag='ACTION', platform='xbox')
    mock_rconn.get.return_value = None
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = game
    result = trending_game()
    assert result.id == 1

@patch('services.library.rconn')
@patch('services.library.Session')
def test_trending_conn_error(mock_session, mock_rconn):
    mock_rconn.get.side_effect = ConnectionError
    with raises(ConnectionError):
        trending_game()