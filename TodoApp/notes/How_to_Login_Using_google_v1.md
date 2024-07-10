# Setting Up Google Sign-in in FastAPI

1. **Create Google OAuth Credentials:**

   - Go to the [Google API Console](https://console.developers.google.com/).
   - Create a new project or use an existing one.
   - Navigate to "Credentials" and create OAuth credentials.
   - Choose "Web application" as the application type.
   - Add `http://localhost:8000` (or your deployment URL) to the authorized redirect URIs.

2. **Install Required Libraries:**

   ```bash
   pip install fastapi python-dotenv httpx python-jose cryptography
   ```

3. **Configure FastAPI with OAuth:**

   - Create a `.env` file and add your Google OAuth credentials:

     ```dotenv
     GOOGLE_CLIENT_ID=your_client_id
     GOOGLE_CLIENT_SECRET=your_client_secret
     ```

   - Load these credentials in your FastAPI application.

4. **Implement Google Sign-in Endpoint:**

   - Create a route in FastAPI to initiate Google Sign-in:

     ```python
     from fastapi import FastAPI, HTTPException, Depends
     from fastapi.security import OAuth2PasswordBearer
     from jose import JWTError, jwt
     from pydantic import BaseModel
     from typing import Optional
     import httpx

     app = FastAPI()

     class GoogleOAuthSettings:
         CLIENT_ID: str = "your_client_id"
         CLIENT_SECRET: str = "your_client_secret"
         REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
         SCOPE: str = "openid email profile"
         TOKEN_ENDPOINT: str = "https://oauth2.googleapis.com/token"
         USERINFO_ENDPOINT: str = "https://www.googleapis.com/oauth2/v1/userinfo"

     # OAuth2 token
     oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

     @app.get("/auth/google")
     async def login_google():
         auth_url = (
             f"https://accounts.google.com/o/oauth2/v2/auth"
             f"?client_id={GoogleOAuthSettings.CLIENT_ID}"
             f"&redirect_uri={GoogleOAuthSettings.REDIRECT_URI}"
             f"&response_type=code"
             f"&scope={GoogleOAuthSettings.SCOPE}"
         )
         return {"auth_url": auth_url}

     @app.get("/auth/google/callback")
     async def google_callback(code: str):
         data = {
             "code": code,
             "client_id": GoogleOAuthSettings.CLIENT_ID,
             "client_secret": GoogleOAuthSettings.CLIENT_SECRET,
             "redirect_uri": GoogleOAuthSettings.REDIRECT_URI,
             "grant_type": "authorization_code",
         }

         async with httpx.AsyncClient() as client:
             response = await client.post(GoogleOAuthSettings.TOKEN_ENDPOINT, data=data)
             access_token = response.json().get("access_token")

             user_info = await client.get(
                 GoogleOAuthSettings.USERINFO_ENDPOINT,
                 headers={"Authorization": f"Bearer {access_token}"}
             )
             user_data = user_info.json()
             # Handle user data as needed, e.g., create a user in your system

             return user_data
     ```

5. **Handle User Data and Security Considerations:**

   - Validate and store user data securely.
   - Use HTTPS to protect data during transit.
   - Implement proper token management and expiration handling.

6. **Test the Google Sign-in:**
   - Start your FastAPI server and navigate to `http://localhost:8000/auth/google`.
   - Follow the Google Sign-in flow and check if the callback returns user data.
