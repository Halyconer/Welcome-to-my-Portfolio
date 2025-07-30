# test_app.py

import json
import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
	# Flask provides a test client for our app
	return app.test_client()

@patch('app.get_bulb')
def test_set_brightness_success(mock_get_bulb, client):
	# Arrange: mock a bulb whose set_brightness just records the call
	fake_bulb = mock_get_bulb.return_value
	calls = []
	fake_bulb.set_brightness = lambda br, effect="smooth", duration=500: calls.append((br, effect, duration))

	# Act: send a valid brightness payload
	response = client.post(
		'/set_brightness',
		data=json.dumps({'brightness': 42}),
		content_type='application/json'
	)

	# Assert: correct status, payload and underlying method call
	assert response.status_code == 200
	body = response.get_json()
	assert body['status'] == 'success'
	assert body['brightness_set'] == 42
	assert calls == [(42, "smooth", 500)]

@patch('app.get_bulb')
def test_set_brightness_missing(mock_get_bulb, client):
	# Act: no brightness field provided
	response = client.post(
		'/set_brightness',
		data=json.dumps({}),
		content_type='application/json'
	)

	# Assert: 400 error for missing parameter
	assert response.status_code == 400
	assert response.get_json()['error'] == 'No brightness provided'

@patch('app.get_bulb')
@pytest.mark.parametrize('payload, error_msg', [
	({'brightness': 'not-an-int'}, 'Brightness must be an integer'),
	({'brightness': 0}, 'Brightness must be between 1 and 100'),
	({'brightness': 101}, 'Brightness must be between 1 and 100'),
])
def test_set_brightness_invalid(mock_get_bulb, client, payload, error_msg):
	# Act: send malformed or out-of-range values
	response = client.post(
		'/set_brightness',
		data=json.dumps(payload),
		content_type='application/json'
	)

	# Assert: each invalid case returns the expected error
	assert response.status_code == 400
	assert response.get_json()['error'] == error_msg

@patch('app.get_bulb', return_value=None)
def test_set_brightness_unreachable(mock_get_bulb, client):
	# Act: brightness valid but bulb unreachable
	response = client.post(
		'/set_brightness',
		data=json.dumps({'brightness': 50}),
		content_type='application/json'
	)

	# Assert: 500 error if we can't get the bulb
	assert response.status_code == 500
	assert response.get_json()['error'] == 'Bulb unreachable'
