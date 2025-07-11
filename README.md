# ♟️ Classifier of Good or Bad Chess Plays

Este proyecto aplica técnicas de inteligencia artificial supervisada para clasificar jugadas de ajedrez como **"buenas" o "malas"** según su impacto en la evaluación de la posición. Se utilizan partidas reales extraídas de [Lichess.org](https://lichess.org) y se evalúan con el motor de ajedrez **Stockfish** para etiquetar las jugadas de forma automática.

---

## 📁 Estructura del proyecto

Classifier-of-good-or-bad-plays/
│
├── Data/                    # Archivos de datos
│   ├── lichess_db_standard_rated_2014-01.pgn  # Dataset original (ignorado en Git)
│   └── parsed_moves.csv     # Salida del procesamiento de jugadas
│
├── Scripts_for_model/       # Scripts de procesamiento y entrenamiento
│   └── extract_fens.py
│
├── requirements.txt         # Dependencias del entorno
├── .gitignore              # Exclusión de archivos grandes y temporales
└── README.md               # Documentación del proyecto

---

## 🚀 Funcionalidades principales

- Procesamiento de archivos PGN de ajedrez.
- Extracción de posiciones FEN y jugadas individuales.
- Evaluación de jugadas con el motor Stockfish.
- Etiquetado de jugadas como "buenas" o "malas".
- Preparación de dataset para entrenar modelos de clasificación.

---

## 📦 Dataset

- **Fuente**: [https://database.lichess.org](https://database.lichess.org)
- **Archivo utilizado**: [lichess_db_standard_rated_2014-01.pgn](https://database.lichess.org/standard/lichess_db_standard_rated_2014-01.pgn.zst)
- **Tamaño**: 111 MB, contiene aproximadamente 697,600 partidas.
- **Nota**: Este archivo está excluido del repositorio por su tamaño. Se recomienda trabajar con un subconjunto inicial de partidas.

---

## 🔍 Subconjunto evaluado

Aunque el archivo `parsed_moves.csv` contiene un total de **656,851 jugadas extraídas**, para propósitos de prueba y eficiencia, actualmente solo se están evaluando **20,000 registros** con Stockfish.

Este valor es **escalable y modificable** fácilmente desde el parámetro `EVAL_LIMIT` en el archivo `Scripts_for_model/evaluate_moves.py`.

Esto permite reducir el tiempo de procesamiento inicial y facilita la validación antes de procesar el conjunto completo.

---

## ⚙️ Requisitos del sistema

- Python 3.9 o superior
- Entorno virtual (recomendado)
- Motor Stockfish (instalado en el sistema y accesible por línea de comandos)
⚠️ Nota: La carpeta `stockfish/` se incluye localmente solo por comodidad, pero está excluida del repositorio por peso y portabilidad. Puedes usar tu propia versión del motor o cambiar la ruta en el script.


Instalación de dependencias:
```bash
pip install -r requirements.txt
