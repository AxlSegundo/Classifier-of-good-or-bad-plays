import pandas as pd
import chess
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


INPUT_CSV = "Classifier-of-good-or-bad-plays/Data/evaluated_moves.csv"

# Codificar piezas a valores enteros (puedes cambiar por 1-hot luego)
PIECE_MAP = {
    'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
    'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6
}

def fen_to_features(fen):
    parts = fen.split()
    board_part, turn, castling, ep_square, halfmove, fullmove = parts

    # Codificar piezas
    board_vec = []
    for row in board_part.split('/'):
        for char in row:
            if char.isdigit():
                board_vec.extend([0] * int(char))
            else:
                board_vec.append(PIECE_MAP.get(char, 0))

    # Turno
    turn_val = 1 if turn == 'w' else 0

    # Castling
    castling_rights = [int(c in castling) for c in "KQkq"]

    # En passant (columna a=0, ..., h=7; si no hay = -1)
    ep_vec = [-1]
    if ep_square != "-":
        ep_vec = [ord(ep_square[0]) - ord('a')]

    # Otros valores
    halfmove = int(halfmove)
    fullmove = int(fullmove)

    return board_vec + [turn_val] + castling_rights + ep_vec + [halfmove, fullmove]

if __name__ == "__main__":
    print("📦 Cargando dataset...")
    df = pd.read_csv(INPUT_CSV)

    print("🔁 Convirtiendo FENs a vectores...")
    features = []
    labels = []
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        try:
            feat = fen_to_features(row["fen"])
            features.append(feat)
            labels.append(row["label"])
        except Exception as e:
            continue

    X = np.array(features)
    y = np.array(labels)

    print(f"✅ Dataset preparado. Tamaño: {X.shape}")

    print("✂️ Dividiendo en entrenamiento y prueba...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    print("🌲 Entrenando modelo Random Forest...")
    clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    clf.fit(X_train, y_train)

    # Evaluación
    print("🧪 Evaluando modelo...")
    y_pred = clf.predict(X_test)

    print("\n📊 Reporte de clasificación:")
    print(classification_report(y_test, y_pred))

    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred)

    # Visualización de la matriz de confusión
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Mala (0)", "Buena (1)"],
                yticklabels=["Mala (0)", "Buena (1)"])
    plt.xlabel("Predicción")
    plt.ylabel("Real")
    plt.title("Matriz de confusión")
    plt.tight_layout()
    plt.show()



    # Guardar el modelo entrenado
    joblib.dump(clf, "Classifier-of-good-or-bad-plays/Models/model_RF.pkl")
    print("💾 Modelo guardado como model_RF.pkl")
