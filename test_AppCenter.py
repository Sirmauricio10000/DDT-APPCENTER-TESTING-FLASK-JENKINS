import requests
import pytest
from mongo_connection import get_mongo_collection

collection = get_mongo_collection()
headers = collection.find_one()["headers"]

#Tests para verificar la informacion del usuario
def test_get_user_verify_username():
    url = f"https://api.appcenter.ms/v0.1/user"

    response = requests.get(url, headers=headers)
    data = response.json()

    expected = collection.find_one()["prueba_1"]["expected"]
    assert data["name"] == expected

######################################################################
def test_get_user_verify_display_name():
    url = f"https://api.appcenter.ms/v0.1/user"

    response = requests.get(url, headers=headers)
    data = response.json()

    expected = collection.find_one()["prueba_2"]["expected"]
    assert data["display_name"] == expected

######################################################################
def test_get_user_verify_mail():
    url = f"https://api.appcenter.ms/v0.1/user"

    response = requests.get(url, headers=headers)
    data = response.json()

    expected = collection.find_one()["prueba_3"]["expected"]
    assert data["email"] == expected

######################################################################





#Tests para crear organizaciones
def test_create_organization_verify_display_name():
    url = f"https://api.appcenter.ms/v0.1/orgs"

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

    payload = collection.find_one()["prueba_6"]["payload"]

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 429:
        pytest.xfail("Exceeded organization creation limit")


    expected = collection.find_one()["prueba_6"]["expected"]
    assert response.status_code == expected

    if response.status_code == expected:
        organization_name = payload["name"]
        delete_organization(organization_name)

######################################################################






#Tests Para crear APPS
def test_create_app_verify_statusCode():
    url = f"https://api.appcenter.ms/v0.1/apps"

    payload = collection.find_one()["prueba_7"]["payload"]

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 429:
        pytest.xfail("Exceeded apps creation limit")

    expected = payload = collection.find_one()["prueba_7"]["expected"]
    assert response.status_code == expected
    
    if response.status_code == expected:
        app_name = payload["name"]
        delete_app("mavendanog", app_name)

######################################################################

def test_create_app_verify_display_name():
    url = f"https://api.appcenter.ms/v0.1/apps"

    payload = collection.find_one()["prueba_8"]["payload"]

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 429:
        pytest.xfail("Exceeded apps creation limit")

    data = response.json()


    expected = collection.find_one()["prueba_8"]["expected"]
    assert data["display_name"] == expected

    if response.status_code == 201:
        app_name = payload["name"]
        delete_app("mavendanog", app_name)

######################################################################

def test_create_app_verify_unauthorized_token():
    url = "https://api.appcenter.ms/v0.1/apps"
    headers = {
        "X-API-Token": collection.find_one()["prueba_9"]["unauthorized_token"],
    }

    payload = collection.find_one()["prueba_9"]["payload"]


    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 429:
        pytest.xfail("Exceeded apps creation limit")


    expected = collection.find_one()["prueba_9"]["expected"]

    assert response.status_code == expected

######################################################################






#Tests Para verificar invitaciones realizadas por el usuario
def test_invitations_unauthorized_token():
    url = "https://api.appcenter.ms/v0.1/invitations/sent"
    headers = {
        "X-API-Token": collection.find_one()["prueba_10"]["unauthorized_token"],
    }

    response = requests.get(url, headers=headers)

    expected = collection.find_one()["prueba_10"]["expected"]
    assert response.status_code == expected

######################################################################

def test_invitations_verify_invitations_sent():
    url = "https://api.appcenter.ms/v0.1/invitations/sent"
    headers = {
        "Accept": "application/json",
        "X-API-Token": "9d99f4f0915046d9a2761c80ce93c522d4e5a5ab",
    }

    response = requests.get(url, headers=headers)
    expected = collection.find_one()["prueba_11"]["expected"]
    
    if len(response.json()) == 0:
        assert len(response.json()) == expected
    else:
        assert len(response.json()) > expected

######################################################################

def test_invitations_verify_status_code():
    url = "https://api.appcenter.ms/v0.1/invitations/sent"

    response = requests.get(url, headers=headers)
    expected = collection.find_one()["prueba_12"]["expected"]

    assert response.status_code == expected

######################################################################









#Tests para verificar las subscripciones azure del usuario
def test_azure_subscriptions_verify_status_code():
    url = "https://api.appcenter.ms/v0.1/azure_subscriptions"

    response = requests.get(url, headers=headers)
    expected = collection.find_one()["prueba_13"]["expected"]

    assert response.status_code == expected

######################################################################

def test_azure_subscriptions_verify_suscriptions():
    url = "https://api.appcenter.ms/v0.1/azure_subscriptions"

    response = requests.get(url, headers=headers)

    expected = collection.find_one()["prueba_14"]["expected"]

    if len(response.json()) == 0:
        assert len(response.json()) == expected
    else:
        assert len(response.json()) > expected

######################################################################

def test_azure_subscriptions_unauthorized_token():
    url = "https://api.appcenter.ms/v0.1/azure_subscriptions"
    headers = {
        "X-API-Token": collection.find_one()["prueba_15"]["unauthorized_token"],
    }

    response = requests.get(url, headers=headers)

    expected = collection.find_one()["prueba_15"]["expected"]
    assert response.status_code == expected

######################################################################









#SubProcesos, NO SON TESTS, son para eliminar los recursos residuales de los test de arriba.

def delete_organization(org_name):
    url = f"https://api.appcenter.ms/v0.1/orgs/{org_name}"

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Organización '{org_name}' eliminada exitosamente.")
    else:
        print(f"No se pudo eliminar la organización '{org_name}'. Código de respuesta: {response.status_code}")


def delete_app(owner_name, app_name):
    url = f"https://api.appcenter.ms/v0.1/apps/{owner_name}/{app_name}"

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"App '{app_name}' eliminada exitosamente.")
    else:
        print(f"No se pudo eliminar la app '{app_name}'. Código de respuesta: {response.status_code}")