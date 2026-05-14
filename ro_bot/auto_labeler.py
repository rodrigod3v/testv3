import cv2
import os
import numpy as np

def auto_label():
    input_dir = "dataset"
    output_dir = "dataset/labels"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("[*] Iniciando Auto-Labeling baseado em diferena de frames...")
    
    # Lista arquivos e ordena por tempo
    files = sorted([f for f in os.listdir(input_dir) if f.endswith(".png")])
    
    if len(files) < 2:
        print("[!] Poucas imagens para comparar.")
        return

    count = 0
    for i in range(1, len(files)):
        img_ant = cv2.imread(os.path.join(input_dir, files[i-1]))
        img_curr = cv2.imread(os.path.join(input_dir, files[i]))
        
        # Calcula diferena para achar o mob
        diff = cv2.absdiff(cv2.cvtColor(img_ant, cv2.COLOR_BGR2GRAY), 
                           cv2.cvtColor(img_curr, cv2.COLOR_BGR2GRAY))
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        labels = []
        h_img, w_img = img_curr.shape[:2]

        for cnt in contours:
            if cv2.contourArea(cnt) > 200: # Filtro de tamanho
                x, y, w, h = cv2.boundingRect(cnt)
                
                # Converte para formato YOLO (normalizado 0-1, centro_x, centro_y, largura, altura)
                x_center = (x + w/2) / w_img
                y_center = (y + h/2) / h_img
                w_norm = w / w_img
                h_norm = h / h_img
                
                # Classe 0 (Mob)
                labels.append(f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}")

        if labels:
            label_file = os.path.join(output_dir, files[i].replace(".png", ".txt"))
            with open(label_file, "w") as f:
                f.write("\n".join(labels))
            count += 1

    print(f"[*] Concludo! {count} arquivos de label gerados em {output_dir}")

if __name__ == "__main__":
    auto_label()
