import requests
import pytest
from mongo_connection import get_mongo_collection

api_token = "9d99f4f0915046d9a2761c80ce93c522d4e5a5ab"
collection = get_mongo_collection()

#Tests para verificar la informacion del usuario
def test_get_user_verify_username():
    url = f"https://api.appcenter.ms/v0.1/user"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    expected = collection.find_one()["prueba_1"]["expected"]
    assert data["name"] == expected

######################################################################
def test_get_user_verify_display_name():
    url = f"https://api.appcenter.ms/v0.1/user"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    expected = collection.find_one()["prueba_2"]["expected"]
    assert data["display_name"] == expected

######################################################################
def test_get_user_verify_mail():
    url = f"https://api.appcenter.ms/v0.1/user"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    expected = collection.find_one()["prueba_3"]["expected"]
    assert data["email"] == expected

######################################################################





#Tests para crear organizaciones
def test_create_organization_verify_display_name():
    url = f"https://api.appcenter.ms/v0.1/orgs"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    payload = collection.find_one()["prueba_4"]["payload"]
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if response.status_code == 429:
        pytest.xfail("Exceeded organization creation limit")

    expected = collection.find_one()["prueba_4"]["expected"]
    assert data["display_name"] == expected

    if response.status_code == 201:
        organization_name = payload["name"]
        delete_organization(organization_name)

######################################################################

def test_create_organization_verify_name():
    url = f"https://api.appcenter.ms/v0.1/orgs"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    payload = collection.find_one()["prueba_5"]["payload"]

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    if response.status_code == 429:
        pytest.xfail("Exceeded organization creation limit")

    expected = collection.find_one()["prueba_5"]["expected"]
    assert data["name"] == expected

    if response.status_code == 201:
        organization_name = payload["name"]
        delete_organization(organization_name)

######################################################################

def test_create_organization_verify_statusCode():
    url = f"https://api.appcenter.ms/v0.1/orgs"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    payload = collection.find_one()["prueba_6"]["payload"]

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 429:
        pytest.xfail("Exceeded organization creation limit")


    expected = payload = collection.find_one()["prueba_6"]["expected"]
    assert response.status_code == expected

    if response.status_code == expected:
        organization_name = payload["name"]
        delete_organization(organization_name)

######################################################################






#Tests Para crear APPS
def test_create_app_verify_statusCode():
    url = f"https://api.appcenter.ms/v0.1/apps"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    payload = {
        "description": "descripcion_prueba",
        "release_type": "Release123",
        "display_name": "app para testing DPP",
        "name": "AppTestingDDP",
        "os": "Android",
        "platform": "Java"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 429:
        pytest.xfail("Exceeded apps creation limit")

    assert response.status_code == 201
    
    if response.status_code == 201:
        app_name = payload["name"]
        delete_app("mavendanog", app_name)

######################################################################

def test_create_app_verify_display_name():
    url = f"https://api.appcenter.ms/v0.1/apps"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    payload = {
        "description": "descripcion_prueba",
        "release_type": "Release123",
        "display_name": "app para testing DPP",
        "name": "AppTestingDDP",
        "os": "Android",
        "platform": "Java"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 429:
        pytest.xfail("Exceeded apps creation limit")

    data = response.json()

    assert data["display_name"] == "app para testing DPP"

    if response.status_code == 201:
        app_name = payload["name"]
        delete_app("mavendanog", app_name)

######################################################################

def test_create_app_verify_unauthorized_token():
    url = "https://api.appcenter.ms/v0.1/apps"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "token_no_autorizado",
    }

    payload = {
        "description": "descripcion_prueba",
        "release_type": "Release123",
        "display_name": "app para testing DPP",
        "name": "AppTestingDDP",
        "os": "Android",
        "platform": "Java"
    }


    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 429:
        pytest.xfail("Exceeded apps creation limit")



    assert response.status_code == 401
    assert response.json()["code"] == "Unauthorized"
    assert "Unauthorized. Correlation ID" in response.json()["message"]

######################################################################






#Tests Para verificar invitaciones realizadas por el usuario
def test_invitations_unauthorized_token():
    url = "https://api.appcenter.ms/v0.1/invitations/sent"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "token_no_autorizado",
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 401
    assert response.json()["code"] == "Unauthorized"
    assert "Unauthorized. Correlation ID" in response.json()["message"]

######################################################################

def test_invitations_verify_invitations_sent():
    url = "https://api.appcenter.ms/v0.1/invitations/sent"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "9d99f4f0915046d9a2761c80ce93c522d4e5a5ab",
    }

    response = requests.get(url, headers=headers)

    if len(response.json()) == 0:
        # No se han enviado invitaciones
        assert response.json() == []
    else:
        # Se han enviado invitaciones
        assert len(response.json()) > 0

######################################################################

def test_invitations_verify_status_code():
    url = "https://api.appcenter.ms/v0.1/invitations/sent"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "9d99f4f0915046d9a2761c80ce93c522d4e5a5ab",
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200

######################################################################









#Tests para verificar las subscripciones azure del usuario
def test_azure_subscriptions_verify_status_code():
    url = "https://api.appcenter.ms/v0.1/azure_subscriptions"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "9d99f4f0915046d9a2761c80ce93c522d4e5a5ab",
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200

######################################################################

def test_azure_subscriptions_verify_suscriptions():
    url = "https://api.appcenter.ms/v0.1/azure_subscriptions"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "9d99f4f0915046d9a2761c80ce93c522d4e5a5ab",
    }

    response = requests.get(url, headers=headers)

    if len(response.json()) == 0:
        # No tiene suscripciones
        assert response.json() == []
    else:
        # Lista de suscrpciones
        assert len(response.json()) > 0

######################################################################

def test_azure_subscriptions_unauthorized_token():
    url = "https://api.appcenter.ms/v0.1/azure_subscriptions"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "token_no_autorizado",
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 401
    assert response.json()["code"] == "Unauthorized"
    assert "Unauthorized. Correlation ID" in response.json()["message"]

######################################################################









#SubProcesos, NO SON TESTS, son para eliminar los recursos residuales de los test de arriba.

def delete_organization(org_name):
    url = f"https://api.appcenter.ms/v0.1/orgs/{org_name}"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Organización '{org_name}' eliminada exitosamente.")
    else:
        print(f"No se pudo eliminar la organización '{org_name}'. Código de respuesta: {response.status_code}")


def delete_app(owner_name, app_name):
    url = f"https://api.appcenter.ms/v0.1/apps/{owner_name}/{app_name}"
    headers = {
        "Accept": "application/json",
        "X-API-Token": api_token,
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"App '{app_name}' eliminada exitosamente.")
    else:
        print(f"No se pudo eliminar la app '{app_name}'. Código de respuesta: {response.status_code}")