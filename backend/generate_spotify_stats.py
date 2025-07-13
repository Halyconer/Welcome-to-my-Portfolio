# backend/generate_spotify_stats.py

import os
import requests
import base64
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1' 

def get_access_token(client_id, client_secret, refresh_token):
    """
    Uses the refresh token to get a new access token from Spotify.
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    
    headers = {
        'Authorization': f"Basic {auth_base64}",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()['access_token']

def get_top_artists(access_token):
    """
    Fetches the user's top artists from the Spotify API.
    """
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    # time_range can be 'short_term' (4 weeks), 'medium_term' (6 months), or 'long_term' (several years)
    # limit is the number of artists to retrieve (max 50)
    params = {
        'time_range': 'short_term',
        'limit': 10 
    }
    response = requests.get(f"{SPOTIFY_API_BASE_URL}/me/top/artists", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def main():
    """
    Main function to orchestrate fetching and saving Spotify stats.
    """
    print("Attempting to fetch Spotify top artists...")

    # 1. Get credentials from environment variables
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("Error: Make sure SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN are set as environment variables.")
        return

    try:
        # 2. Get a fresh access token
        access_token = get_access_token(client_id, client_secret, refresh_token)
        print("Successfully obtained a new access token.")

        # 3. Fetch top artists
        top_artists_data = get_top_artists(access_token)
        print(f"Successfully fetched {len(top_artists_data.get('items', []))} top artists.")

        # 4. Format the data for the frontend
        output_data = {
            'last_updated_utc': datetime.utcnow().isoformat(),
            'artists': []
        }

        for artist in top_artists_data.get('items', []):
            output_data['artists'].append({
                'name': artist['name'],
                'image_url': artist['images'][0]['url'] if artist['images'] else None,
            })
        
        # 5. Write the data to a JSON file
        output_filename = 'spotify_top_artists.json'
        with open(output_filename, 'w') as f:
            json.dump(output_data, f, indent=4)
        
        print(f"✅ Successfully saved top artists data to {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        if e.response:
            print("Response content:", e.response.text)

if __name__ == '__main__':
    main()
