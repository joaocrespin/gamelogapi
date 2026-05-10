from unittest.mock import patch
from services.library import trending_game
from services.recommendation import recommend_games
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


@patch('services.recommendation.Session')
@patch('services.recommendation._search_all_user_games')
@patch('services.recommendation._search_game_tags')
@patch('services.recommendation._search_user_highest_rated_games')
def test_recommendation(mock_highest_rated, mock_all_user_games, mock_game_tags, mock_session):
    game = Game(id=4, name='Action Game', description='fast paced', tag='ACTION', platform='xbox')
    mock_highest_rated.return_value = [1, 2, 3] 
    mock_all_user_games.return_value = [1, 2, 3, 5, 6] 
    mock_game_tags.return_value = ['ACTION']
    mock_session.return_value.__enter__.return_value.execute.return_value.scalars.return_value.all.return_value = [game]

    result = recommend_games(1)
    assert result[0].id == 4

@patch('services.recommendation._search_user_highest_rated_games')
def test_recommendation_no_games(mock_highest_rated):
    mock_highest_rated.return_value = []
    with raises(ValueError):
        recommend_games(1)

@patch('services.recommendation._search_user_highest_rated_games')
def test_recommendation_no_reviews(mock_highest_rated):
    mock_highest_rated.return_value = None
    with raises(ValueError):
        recommend_games(1)