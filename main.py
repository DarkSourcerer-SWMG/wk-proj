import cv2
import os
import numpy as np

# --- 1. KONFIGURACJA ŚCIEŻEK  ---
FOLDER_PATH = r"Crowd_PETS09\S2\L1\Time_12-34\View_001"

def load_dataset(path):
    if not os.path.exists(path):
        print(f"BŁĄD: Folder {path} nie istnieje!")
        return []
    images = sorted([img for img in os.listdir(path) if img.endswith((".jpg", ".png"))])
    return images

# --- 2. KONFIGURACJA BRAMKI PIONOWEJ  ---
LINE_X = 150        # Położenie pionowej linii (150 pikseli od lewej edge)
LINE_Y_MIN = 0    # Górna granica linii (poczatek chodnika w oddali)
LINE_Y_MAX = 560    # Dolna granica linii (blisko dolnej krawędzi)
OFFSET = 15         # Szerokość "strefy" zliczania (tolerancja w px)

counter = 0
counted_ids = set()   # Zbiór ID już policzonych
tracked_objects = {}  # Aktywne obiekty {id: (cx, cy)}
next_id = 0

# --- 3. DETEKCJA  ---
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

image_list = load_dataset(FOLDER_PATH)

print(f"System gotowy. Przetwarzanie sekwencji: {len(image_list)} klatek.")

# GŁÓWNA PĘTLA PRZETWARZANIA
for img_name in image_list:
    frame = cv2.imread(os.path.join(FOLDER_PATH, img_name))
    if frame is None:
        continue

    # --- KROK 1: PREPROCESSING  ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # --- KROK 2: DETEKCJA  ---
    mask = fgbg.apply(blur)
    _, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY) # Usuwanie cieni
    
    # Morfologia - poprawia spójność sylwetek
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    current_centroids = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 600 < area < 15000: # Ignorujemy szum i zbyt wielkie plamy
            x, y, w, h = cv2.boundingRect(cnt)
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            current_centroids.append((cx, cy, x, y, w, h))

    # --- KROK 3: TRACKING  ---
    new_tracked_objects = {}
    for (cx, cy, x, y, w, h) in current_centroids:
        closest_id = None
        min_dist = float('inf')
        
        # Przypisujemy ID na podstawie odległości od poprzedniej klatki
        for obj_id, old_pos in tracked_objects.items():
            dist = np.hypot(cx - old_pos[0], cy - old_pos[1])
            if dist < 50 and dist < min_dist:
                min_dist = dist
                closest_id = obj_id

        if closest_id is None:
            obj_id = next_id
            next_id += 1
        else:
            obj_id = closest_id
        
        new_tracked_objects[obj_id] = (cx, cy)

        # --- KROK 4: LOGIKA BRAMKI PIONOWEJ  ---
        if obj_id not in counted_ids:
            # Sprawdzamy czy środek X jest blisko linii ORAZ czy Y jest w zakresie chodnika
            if abs(cx - LINE_X) < OFFSET and LINE_Y_MIN < cy < LINE_Y_MAX:
                counter += 1
                counted_ids.add(obj_id)
                print(f"Osoba ID:{obj_id} przekroczyła pionową linię! Suma: {counter}")

        # Wizualizacja ramki i ID
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{obj_id}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    tracked_objects = new_tracked_objects

    # --- KROK 5: WIZUALIZACJA  ---
    # Rysowanie niebieskiej bramki pionowej
    cv2.line(frame, (LINE_X, LINE_Y_MIN), (LINE_X, LINE_Y_MAX), (255, 0, 0), 3)
    
    # Czarny pasek statystyk
    cv2.rectangle(frame, (0, 0), (280, 50), (0, 0, 0), -1)
    cv2.putText(frame, f"Liczba osob: {counter}", (10, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.imshow('System Liczenia - Bramka Pionowa', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print(f"Zakończono. Łącznie wykryto osób: {counter}")
