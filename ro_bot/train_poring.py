from ultralytics import YOLO
import os

def treinar_poring():
    # O Roboflow j entrega o arquivo 'data.yaml' pronto na pasta baixada
    # Certifique-se de que a pasta se chama 'poring_dataset'
    data_yaml = os.path.abspath("poring_dataset/data.yaml")
    
    if not os.path.exists(data_yaml):
        print("[!] Erro: No encontrei o arquivo 'data.yaml' em poring_dataset/.")
        print("[!] Certifique-se de baixar o dataset do Roboflow em formato YOLOv8 e extrair aqui.")
        return

    print("[*] Iniciando treinamento do PORING EXPERT...")
    # Carrega o modelo base
    model = YOLO("yolov8n.pt")
    
    # Treina (50 pocas  o ideal para comear)
    # Se voc tiver uma GPU Nvidia, mude device='cpu' para device=0
    model.train(data=data_yaml, epochs=50, imgsz=640, device="cpu", name="poring_model")
    
    print("\n[!] Treinamento concludo!")
    print("[!] O modelo final est em: runs/detect/poring_model/weights/best.pt")

if __name__ == "__main__":
    treinar_poring()
