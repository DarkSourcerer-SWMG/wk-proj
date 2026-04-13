
# 🚶‍♂️ System Detekcji i Liczenia Osób (Bramka Pionowa)

### Projekt na przedmiot: Współczesne Kierunki Informatyki (Semestr 6)
### Dataset: PETS 2009

---

## 📋 Opis Projektu
Celem projektu jest automatyczne zliczanie osób przekraczających wirtualną, pionową linię kontrolną. System przetwarza sekwencje obrazów ze zbioru danych **PETS2009**, wykorzystując algorytmy odejmowania tła (Background Subtraction) oraz śledzenia obiektów (Object Tracking) w czasie rzeczywistym.

## 👥 Zespół Projektowy
Program został podzielony na moduły, za które odpowiadali poszczególni członkowie zespołu:
* **Bartosz Zając** – Konfiguracja ścieżek dostępu, wczytywanie datasetu oraz preprocessing obrazu (skalowanie, konwersja barw, rozmycie Gaussa).
* **Gabriel Solarz** – Implementacja detekcji ruchu przy użyciu algorytmu MOG2 oraz filtracja morfologiczna masek binarnych.
* **Miłosz Hart** – Opracowanie algorytmu śledzenia (tracking) opartego na odległości euklidesowej między centroidami obiektów.
* **Bartłomiej Sitek** – Logika bramki pionowej (zliczanie po przekroczeniu X), opracowanie interfejsu graficznego (UI) oraz wizualizacja statystyk.

---

## 🚀 Szybki Start (Setup)

### 1. Klonowanie repozytorium

git clone https://github.com/DarkSourcerer-SWMG/wk-proj
cd wk-proj
```

### 2. Instalacja zależności
Zalecane jest użycie środowiska wirtualnego:

# Tworzenie i aktywacja środowiska
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalacja bibliotek
pip install opencv-python numpy
```

### 3. Przygotowanie danych (PETS2009)
Ze względu na rozmiar, dane nie są częścią repozytorium.
1. Pobierz sekwencję **S2: People Tracking** -> **L1: Low and medium density** -> **View 001** ze strony [PETS 2009 Benchmark Data](http://www.cvg.reading.ac.uk/PETS2009/a.html).
2. Rozpakuj zdjęcia do folderu wewnątrz projektu według poniższej struktury:

   Twoj-Projekt/
   ├── data/
   │   └── S2_L1/
   │       └── View_001/
   │           ├── frame_0000.jpg
   │           └── ...
   ├── main.py
   └── README.md
   ```

---

## 🛠️ Logika działania
System realizuje przetwarzanie w pięciu głównych krokach:
1. **Preprocessing**: Konwersja do skali szarości i redukcja szumów (Gaussian Blur).
2. **Detekcja**: Wykorzystanie `MOG2` do wyodrębnienia poruszających się obiektów (usuwanie cieni).
3. **Morfologia**: Operacja dylatacji w celu połączenia rozłączonych fragmentów sylwetek.
4. **Tracking**: Przypisywanie ID na podstawie najmniejszej odległości euklidesowej między klatkami.
5. **Bramka**: Weryfikacja współrzędnej `X` centroidu względem linii `LINE_X` w zadanym zakresie wysokości `Y`.

## ⚙️ Parametry Konfiguracyjne
Wszystkie kluczowe ustawienia znajdują się w górnej sekcji pliku `main.py`:
* `LINE_X = 150` – Pozycja pionowej linii zliczania.
* `OFFSET = 15` – Szerokość strefy detekcji (px).
* `area > 600` – Minimalna wielkość obiektu (filtrowanie szumów).

---
*Projekt realizowany na potrzeby akademickie. Pamiętaj o dodaniu folderu `data/` do pliku .gitignore przed wysłaniem kodu na serwer.*
```
