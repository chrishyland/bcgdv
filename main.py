import json
import requests
from requests import HTTPError

BASE_URI = r'https://interns.bcgdvsydney.com'
name = 'Charles Hyland'
email = 'chyl9109@uni.sydney.edu.au'

def retrieve_api_key() -> str:
    """
    Make a GET request to retrieve API key.

    Returns:
    result: str
        The api key.
    """
    url = f"{BASE_URI}/api/v1/key"
    api_key = ' '
    try:
        response = requests.get(url=url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:        
        if response.status_code == 201:
            response.encoding = 'utf-8'
            json_response = response.json()
            api_key = json_response['key']
        elif response.status_code == 404:
            print('Response not found.')
        else:
            print('Other response error.')

    return api_key


def submit_application(api_key: str,name: str,email: str) -> str:
    """
    Makes a HTTP post request to submit application.

    Parameters:
    --------
    api_key: str
        API key generated from retrieve_api_key function.

    Returns:
    response_result: json
        The json response from the submission.
    """
    response_result = None
    url = f'{BASE_URI}/api/v1/submit?apiKey={api_key}'
    print(url)
    payload = {'apiKey': api_key, 'name': name, 'email': email}
    try:
        # JSON keyword changes Content-Type header to application/JSON.
        response = requests.post(url=url, json=payload) 
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:        
        if response.status_code == 202:
            response.encoding = 'utf-8'
            json_response = response.json()
            response_result = json_response
        else:
            print('Response error with submission.')
    return response_result


def main():
    api_key = retrieve_api_key()
    if not api_key.isspace():
        app_response = submit_application(api_key, name, email)
    else:
        print('Failure to generate api key.')
    
    if app_response is not None:
        print(app_response)
    else:
        print('Failure to submit application.')


if __name__ == '__main__':
    main()