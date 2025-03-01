import json
import os

class AIEngine:
    def __init__(self):
        self.bins_validos_path = 'data/bins_validos.json'
        self.cc_validas_path = 'data/cc_validas.json'
        os.makedirs('data', exist_ok=True)

    def registrar_bin_exitoso(self, bin_code):
        print(f"BIN válido registrado: {bin_code}")

    def registrar_bin_fallido(self, bin_code):
        print(f"BIN fallido: {bin_code}")

    def guardar_bin(self, bin_data):
        bins = self.cargar_bins_validos()
        bins.append(bin_data)
        self._guardar_json(self.bins_validos_path, bins)

    def cargar_bins_validos(self):
        return self._cargar_json(self.bins_validos_path)

    def registrar_cc_exitosa(self, cc):
        print(f"CC válida registrada: {cc}")

    def registrar_cc_fallida(self, cc):
        print(f"CC fallida: {cc}")

    def guardar_cc(self, cc_data):
        ccs = self._cargar_json(self.cc_validas_path)
        ccs.append(cc_data)
        self._guardar_json(self.cc_validas_path, ccs)

    def _cargar_json(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return []

    def _guardar_json(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
