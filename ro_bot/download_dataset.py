from roboflow import Roboflow
import os

# SUBSTITUA PELA SUA CHAVE DO ROBOFLOW
API_KEY = "SUA_API_KEY_AQUI"

def baixar():
    rf = Roboflow(api_key=API_KEY)
    # Configurado para o dataset que voc encontrou
    project = rf.workspace("pdiaps").project("poring")
    version = project.version(1)
    
    # Baixa no formato YOLOv8
    dataset = version.download("yolov8")
    
    print(f"[*] Dataset baixado em: {dataset.location}")
    print("[*] Agora você pode mover as imagens para sua pasta 'dataset' ou treinar direto desta pasta.")

if __name__ == "__main__":
    if API_KEY == "SUA_API_KEY_AQUI":
        print("[!] Por favor, coloque sua API KEY do Roboflow no arquivo.")
    else:
        baixar()
