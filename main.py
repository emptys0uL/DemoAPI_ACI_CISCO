import json
import requests
import conf

sandbox = "https://sandboxapicdc.cisco.com"


def obtener_token(usuario, clave):
    url = sandbox + "/api/aaaLogin.json"
    body = {
        "aaaUser": {
            "attributes": {
                "name": usuario,
                "pwd": clave
            }
        }
    }
    cabecera = {
        "Content-Type": "application/json"
    }
    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']
    return token


# GET http://apic-ip-address/api/class/topSystem.json

def top_system():
    cabecera = {
        "Content-Type": "application/json"
    }
    galleta = {
        "APIC-Cookie": obtener_token(conf.usuario, conf.clave)
    }

    requests.packages.urllib3.disable_warnings()
    respuesta = requests.get(sandbox+"/api/class/topSystem.json", headers=cabecera, cookies=galleta, verify=False)

    total_nodos = int(respuesta.json()["totalCount"])

    for i in range(0, total_nodos):
        ip_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["address"]
        print(ip_local)

top_system()