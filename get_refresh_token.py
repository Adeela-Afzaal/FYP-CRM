from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRETS_FILE = 'client_secret.json'

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

auth_url, _ = flow.authorization_url(prompt='consent')
print('Go to this URL:\n', auth_url)

code = input('Enter the authorization code: ')
flow.fetch_token(code=code)

print('Refresh token:', flow.credentials.refresh_token)
