import requests
import json
import re


class Requester:
	HOST = 'http://127.0.0.1'
	BASE_HTTP_ERROR = (json.dumps({'error': 'BaseHTTPError'}), 500)

	def get_request(self, url, headers: dict={}):
		try:
			response = requests.get(url, headers=headers)
		except (requests.exceptions.BaseHTTPError, requests.exceptions.ConnectionError):
			return None
		return response

	def post_request(self, url, data, headers: dict={}):
		try:
			response = requests.post(url=url, json=data, headers=headers)
		except (requests.exceptions.BaseHTTPError, requests.exceptions.ConnectionError):
			return None
		return response

	def patch_request(self, url, data, headers: dict={}):
		try:
			response = requests.patch(url=url, json=data, headers=headers)
		except (requests.exceptions.BaseHTTPError, requests.exceptions.ConnectionError):
			return None
		return response

	def delete_request(self, url, headers: dict={}):
		try:
			response = requests.delete(url=url, headers=headers)
		except (requests.exceptions.BaseHTTPError, requests.exceptions.ConnectionError):
			return None
		return response

	def get_data_from_response(self, response):
		try:
			return response.json()
		except (ValueError, json.JSONDecodeError, AttributeError):
			return response.text

	def get_token_from_request(self, request):
		try:
			token = request.META['HTTP_AUTHORIZATION']
			if token[0] == '{':
				return token
			else:
				return token[7:]
		except (IndexError, KeyError):
			return None
