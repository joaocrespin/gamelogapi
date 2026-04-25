from unittest.mock import patch
from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from services.review import create_review, read_review, update_review, delete_review
from models.review import Review
from pytest import raises

def refresh(obj):
    obj.id = 1

@patch('services.review.Session')
def test_create_review(mock_session):
    mock_session.return_value.__enter__.return_value.refresh.side_effect = refresh
    new_review = ReviewCreate(game_id=1, stars=5, review='very cool')
    result = create_review(new_review, 1)
    assert result.id == 1

@patch('services.review.Session')
def test_read_review(mock_session):
    review = Review(id=1, user_id=1, game_id=1, stars=5, review='very cool')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = review
    result = read_review(1)
    assert result.stars == 5

@patch('services.review.Session')
def test_update_review(mock_session):
    review = Review(id=1, user_id=1, game_id=1, stars=5, review='very cool')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = review
    result = update_review(ReviewUpdate(id=1, stars=1, review='low-key mid'))
    assert result.id == 1

@patch('services.review.Session')
def test_delete_review(mock_session):
    review = Review(id=1, user_id=1, game_id=1, stars=5, review='very cool')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = review
    result = delete_review(1)
    assert result == True

@patch('services.review.Session')
def test_failed_read_review(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = read_review(1)

@patch('services.review.Session')
def test_failed_update_review(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = update_review(ReviewUpdate(id=1, stars=1, review='low-key mid'))

@patch('services.review.Session')
def test_failed_delete_review(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = delete_review(1)
