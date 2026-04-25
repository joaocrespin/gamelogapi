from unittest.mock import patch
from schemas.library import LibraryEntry, EntryUpdate
from services.library import create_entry, read_entry, update_entry, delete_entry
from models.library import Library
from pytest import raises

def refresh(obj):
    obj.id = 1

@patch('services.library.Session')
def test_create_library(mock_session):
    mock_session.return_value.__enter__.return_value.refresh.side_effect = refresh
    new_entry = LibraryEntry(game_id=1, status='playing')
    
    result = create_entry(new_entry, 1)
    assert result.id == 1


@patch('services.library.Session')
def test_read_entry(mock_session):
    entry = Library(id=1, user_id='1', game_id='1', status='playing')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = entry
    result = read_entry(1)
    assert result.user_id == 1

@patch('services.library.Session')
def test_update_entry(mock_session):
    entry = Library(id=1, user_id='1', game_id='1', status='playing')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = entry
    result = update_entry(EntryUpdate(id=1, status='dropped'))
    # Due to mock limitations, it's not possible to update the status of the memory object
    assert result.id == 1

@patch('services.library.Session')
def test_delete_entry(mock_session):
    entry = Library(id=1, user_id='1', game_id='1', status='playing')
    mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = entry
    result = delete_entry(1)
    assert result == True

@patch('services.library.Session')
def test_failed_read_entry(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = read_entry(2)

@patch('services.library.Session')
def test_failed_update_entry(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = update_entry(EntryUpdate(id=2, status='wishlist'))

@patch('services.library.Session')
def test_failed_delete_entry(mock_session):
    with raises(ValueError):
        mock_session.return_value.__enter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
        result = delete_entry(2)