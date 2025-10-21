# get_token.py (NEW Server Method)

import praw
import sys
import webbrowser
import socket
import random

def get_refresh_token():
    """
    A one-time script to get a Reddit refresh token by running a
    temporary local web server.
    """
    print("--- Reddit Refresh Token Generator (Server Method) ---")

    # 1. Get user input for credentials
    client_id = input("Enter your Reddit App Client ID: ").strip()
    client_secret = input("Enter your Reddit App Client Secret: ").strip()
    redirect_uri = "http://localhost:8080"
    
    # Check that the redirect_uri in app settings is correct
    print("\nIMPORTANT: Please double-check your Reddit App settings:")
    print(f"Make sure your 'redirect uri' is set to EXACTLY: {redirect_uri}")
    input("Press ENTER to continue if this is correct...")
    
    # Define the permissions our bot needs
    scopes = ["identity", "read", "submit"]
    state = str(random.randint(0, 65000))

    try:
        # 2. Initialize PRAW
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            user_agent="Token Grabber (server method)"
        )
        
        # 3. Generate the authorization URL
        auth_url = reddit.auth.url(scopes=scopes, state=state, duration="permanent")
        
        print("\n--- ACTION REQUIRED ---")
        print("1. A browser window will now open.")
        print("2. Log in to your Reddit account (use your Google SSO).")
        print("3. Click 'Allow' to authorize the app.")
        print("4. You will be redirected. The script will catch the code automatically.")
        print("\nWaiting for authorization code...")

        webbrowser.open(auth_url)

        # 4. Start a local server to listen for the redirect
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 8080))
        server.listen(1)
        client, _ = server.accept()
        
        # 5. Receive the data from the browser
        data = client.recv(1024).decode("utf-8")
        
        # Send a response to the browser to close the connection
        response = "HTTP/1.1 200 OK\n\n<html><body>Token received. You can close this window.</body></html>"
        client.sendall(response.encode("utf-8"))
        client.close()
        server.close()

        # 6. Parse the 'code' and 'state' from the browser data
        # Data looks like: GET /?state=...&code=... HTTP/1.1
        try:
            query_params = data.split(" ")[1].split("?")[1]
            params = dict(param.split("=") for param in query_params.split("&"))
            
            received_code = params["code"]
            received_state = params["state"]
        except Exception:
            print("\nError: Could not parse the code from the browser.")
            print("Please make sure you are not running another server on port 8080.")
            return

        # 7. Check if the 'state' matches to prevent CSRF
        if received_state != state:
            print("\nError: State mismatch. Please try running the script again.")
            return

        print("\nAuthorization code received! Fetching refresh token...")
        
        # 8. Exchange the code for the refresh token
        refresh_token = reddit.auth.authorize(received_code)
        
        print("\n--- SUCCESS! ---")
        print("Your Refresh Token is:")
        print(f"\n{refresh_token}\n")
        print("Please copy this token and save it in your .env file. Do NOT share it.")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your Client ID, Client Secret, and that the Redirect URI is correct in your app settings.")

if __name__ == "__main__":
    get_refresh_token()