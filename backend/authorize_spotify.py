import requests
import base64
from urllib.parse import urlencode, parse_qs, urlparse

REDIRECT_URI = 'http://127.0.0.1:5001/callback'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

def get_refresh_token():
    """
    A one-time script to perform the OAuth 2.0 Authorization Code Flow
    and retrieve a refresh token for your Spotify application.
    """
    # 1. Get credentials from the user
    client_id = input("Enter your Spotify Client ID: ").strip()
    client_secret = input("Enter your Spotify Client Secret: ").strip()

    # 2. Construct the authorization URL
    scope = 'user-top-read'  # This scope allows reading the user's top artists and tracks
    
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope,
    }
    
    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(auth_params)}"

    # 3. Prompt the user to authorize the application
    print("\n--- Step 1: Authorize this application ---")
    print("1. Go to the following URL in your browser:")
    print(f"\n   {auth_url}\n")
    print("2. Log in to Spotify if you aren't already.")
    print("3. You will be asked to grant permission. Click 'Agree'.")
    print("4. Your browser will be redirected to a URL that might look like it failed.")
    print("   This is expected. Copy the FULL URL from your browser's address bar.")

    # 4. Get the redirected URL from the user
    redirected_url = input("\n--- Step 2: Paste the full redirected URL here ---\n> ").strip()

    # 5. Extract the authorization code from the URL
    try:
        parsed_url = urlparse(redirected_url)
        query_params = parse_qs(parsed_url.query)
        auth_code = query_params.get('code', [None])[0]
        
    except Exception as e:
        print(f"\nAn error occurred while parsing the URL: {e}")
        return

    # 6. Exchange the authorization code for an access token and refresh token
    print("\n--- Step 3: Exchanging authorization code for a refresh token ---")
    
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    token_payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
    }

    token_headers = {
        'Authorization': f"Basic {auth_base64}",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        response = requests.post(SPOTIFY_TOKEN_URL, data=token_payload, headers=token_headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        token_info = response.json()

        refresh_token = token_info.get('refresh_token')

        if refresh_token:
            print("\n✅ Success! Here is your Refresh Token:")
            print("=" * 50)
            print(refresh_token)
            print("=" * 50)
            print("\nIMPORTANT: Store this token securely. You will need it for your backend script.")
        else:
            print("\n❌ Error: Could not retrieve the refresh token.")
            print("Spotify's response did not include a refresh_token. Please try the process again.")
            print("Response:", token_info)

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred while requesting the token: {e}")
        print("Response content:", e.response.text if e.response else "No response")

if __name__ == '__main__':
    get_refresh_token()
