import requests

def verificar_bin(bin_code, api_key):
    url = f"https://api.bincodes.com/bin/?format=json&api_key={api_key}&bin={bin_code}"
    resp = requests.get(url).json()

    return {
        "bin": bin_code,
        "tipo": resp.get('card_type', 'N/A'),
        "marca": resp.get('card', 'N/A'),
        "banco": resp.get('bank', 'N/A'),
        "pais": resp.get('country', 'N/A'),
        "valido": bool(resp.get('valid', False))
    }

def generar_cc(bin, api_key):
    url = f"https://api.bincodes.com/cc-gen/?format=json&api_key={api_key}&input={bin}"
    resp = requests.get(url).json()
    return resp.get('card_number')

def verificar_cc(cc, api_key):
    url = f"https://api.bincodes.com/cc/?format=json&api_key={api_key}&cc={cc}"
    resp = requests.get(url).json()

    return {
        "numero": cc,
        "tipo": resp.get('card_type', 'N/A'),
        "marca": resp.get('card', 'N/A'),
        "banco": resp.get('bank', 'N/A'),
        "pais": resp.get('country', 'N/A'),
        "valido": bool(resp.get('valid', False))
    }
