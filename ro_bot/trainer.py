import os
import shutil
import random
from ultralytics import YOLO

def preparar_dataset():
    # Estrutura de pastas que o YOLO exige
    base_path = "dataset_yolo"
    dirs = [
        "dataset_yolo/train/images", "dataset_yolo/train/labels",
        "dataset_yolo/val/images", "dataset_yolo/val/labels"
    ]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    # Coleta arquivos originais
    images = [f for f in os.listdir("dataset") if f.endswith(".png")]
    random.shuffle(images)

    # Separa 80% para treino e 20% para validao
    split = int(len(images) * 0.8)
    train_imgs = images[:split]
    val_imgs = images[split:]

    def mover_arquivos(img_list, target_type):
        for img_name in img_list:
            label_name = img_name.replace(".png", ".txt")
            src_img = os.path.join("dataset", img_name)
            src_label = os.path.join("dataset/labels", label_name)
            
            if os.path.exists(src_label):
                shutil.copy(src_img, f"dataset_yolo/{target_type}/images/{img_name}")
                shutil.copy(src_label, f"dataset_yolo/{target_type}/labels/{label_name}")

    print("[*] Organizando arquivos para o YOLO...")
    mover_arquivos(train_imgs, "train")
    mover_arquivos(val_imgs, "val")

    # Cria o arquivo de configurao .yaml
    yaml_content = f"""
path: {os.path.abspath("dataset_yolo")}
train: train/images
val: val/images

names:
  0: Mob
"""
    with open("dataset.yaml", "w") as f:
        f.write(yaml_content)
    print("[*] dataset.yaml criado.")

def treinar():
    preparar_dataset()
    
    print("[*] Iniciando Treinamento da IA (Isso pode demorar alguns minutos)...")
    # Carrega o modelo base nano (leve)
    model = YOLO("yolov8n.pt")
    
    # Inicia o treino
    model.train(data="dataset.yaml", epochs=50, imgsz=640, device="cpu") # Use 'cpu' se no tiver GPU Nvidia
    print("[!] Treinamento concludo! O melhor modelo est em runs/detect/train/weights/best.pt")

if __name__ == "__main__":
    treinar()
