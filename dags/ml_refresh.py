import requests
from google.cloud import secretmanager

SECRET_PROJECT_ID = 'lanch-sync'
REFRESH_TOKEN_SECRET = 'ML_REFRESH_TOKEN_CUENTA1'
CLIENT_ID_SECRET = 'ML_CLIENT_ID_CUENTA1'
CLIENT_SECRET_SECRET = 'ML_CLIENT_SECRET_CUENTA1'
ACCESS_TOKEN_SECRET = 'ML_ACCESS_TOKEN_CUENTA1'

def refresh_token():
    client = secretmanager.SecretManagerServiceClient()

    def access_secret(secret_id):
        name = f"projects/{SECRET_PROJECT_ID}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(name=name)
        value = response.payload.data.decode("UTF-8")
        return value

    refresh_token = access_secret(REFRESH_TOKEN_SECRET)
    client_id = access_secret(CLIENT_ID_SECRET)
    client_secret = access_secret(CLIENT_SECRET_SECRET)

    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()
    new_data = response.json()

    access_token = new_data["access_token"]
    client.add_secret_version(
        request={
            "parent": f"projects/{SECRET_PROJECT_ID}/secrets/{ACCESS_TOKEN_SECRET}",
            "payload": {"data": access_token.encode("UTF-8")}
        }
    )

    new_refresh_token = new_data.get("refresh_token")
    if new_refresh_token:
        client.add_secret_version(
            request={
                "parent": f"projects/{SECRET_PROJECT_ID}/secrets/{REFRESH_TOKEN_SECRET}",
                "payload": {"data": new_refresh_token.encode("UTF-8")}
            }
        )
