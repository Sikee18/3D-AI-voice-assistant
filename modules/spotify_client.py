import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config

class SpotifyController:
    def __init__(self):
        self.sp = None
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=Config.SPOTIPY_CLIENT_ID,
                client_secret=Config.SPOTIPY_CLIENT_SECRET,
                redirect_uri=Config.SPOTIPY_REDIRECT_URI,
                scope="user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"
            ))
        except Exception as e:
            print(f"Spotify Auth Error: {e}")

    def play_music(self, query=None):
        if self.sp:
            try:
                uri = None
                if query:
                    results = self.sp.search(q=query, limit=1, type='track,artist')
                    if results['tracks']['items']:
                        uri = results['tracks']['items'][0]['uri']
                        name = results['tracks']['items'][0]['name']
                        artist = results['tracks']['items'][0]['artists'][0]['name']
                        print(f"Found: {name} by {artist} ({uri})")
                
                # Try to play via API first (if Premium)
                if uri:
                    self.sp.start_playback(uris=[uri])
                    return f"Playing {name} by {artist}."
                else:
                    self.sp.start_playback()
                    return "Resuming music."
                    
            except spotipy.exceptions.SpotifyException as e:
                # Handle Premium restriction or other errors
                if (e.http_status == 403 and "PREMIUM_REQUIRED" in str(e)) or uri:
                    # Fallback or Direct Launch: Open Spotify app via protocol
                    import os
                    if uri:
                        os.startfile(uri) # Opens spotify:track:... directly in app
                        return f"Opening {name} in Spotify app."
                    else:
                        os.startfile("spotify:") # Just open app
                        return "Opening Spotify app."
                return f"Error playing music: {e}"
            except Exception as e:
                # General fallback
                import os
                if uri:
                    os.startfile(uri)
                    return f"Opening {name} in Spotify app."
                return f"Error playing music: {e}"
        return "Spotify not connected."

    def pause_music(self):
        if self.sp:
            try:
                self.sp.pause_playback()
                return "Pausing music."
            except Exception as e:
                print(f"Spotify Pause Error: {e}")
                # Fallback: Use system media keys
                try:
                    import pyautogui
                    pyautogui.press('playpause')
                    return "Pausing music (via system)."
                except:
                    return f"Error pausing music: {e}"
        return "Spotify not connected."

    def next_track(self):
        if self.sp:
            try:
                self.sp.next_track()
                return "Skipping to next track."
            except Exception as e:
                print(f"Spotify Skip Error: {e}")
                # Fallback: Use system media keys
                try:
                    import pyautogui
                    pyautogui.press('nexttrack')
                    return "Skipping track (via system)."
                except:
                    return f"Error skipping track: {e}"
        return "Spotify not connected."

    def add_to_queue(self, query):
        if self.sp:
            try:
                uri = None
                if query:
                    results = self.sp.search(q=query, limit=1, type='track')
                    if results['tracks']['items']:
                        uri = results['tracks']['items'][0]['uri']
                        name = results['tracks']['items'][0]['name']
                        artist = results['tracks']['items'][0]['artists'][0]['name']
                        
                        self.sp.add_to_queue(uri)
                        return f"Added {name} by {artist} to queue."
                return "I couldn't find that song to add."
            except Exception as e:
                return f"Error adding to queue (Premium required): {e}"
        return "Spotify not connected."
