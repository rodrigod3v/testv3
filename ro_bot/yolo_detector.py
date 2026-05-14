from ultralytics import YOLO
import cv2
import numpy as np

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):
        """
        Inicializa o detector YOLO.
        Se o model_path no existir, ele baixar o modelo nano oficial (que  rpido).
        """
        print(f"[*] Carregando modelo YOLO: {model_path}...")
        self.model = YOLO(model_path)
        
    def detectar(self, frame, conf_threshold=0.5):
        """
        Realiza a deteco no frame e retorna uma lista de mobs.
        Retorna: [(cx, cy, conf, label)]
        """
        results = self.model(frame, conf=conf_threshold, verbose=False)
        mobs = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Pegamos as coordenadas do bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = self.model.names[cls]
                
                # No Ragnarok, se voc treinar, o label seria 'poring', 'fabre', etc.
                # Por enquanto, ele vai detectar o que o modelo base conhece (pessoa, cadeira, etc)
                mobs.append((cx, cy, conf, label))
                
        return mobs

    def desenhar_deteccoes(self, frame, mobs):
        """Desenha as boxes na tela para o Debug."""
        for (cx, cy, conf, label) in mobs:
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, f"{label} {conf:.2f}", (cx, cy-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return frame
