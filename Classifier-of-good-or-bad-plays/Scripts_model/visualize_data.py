import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

INPUT_CSV = "Classifier-of-good-or-bad-plays/Data/evaluated_moves.csv"

if __name__ == "__main__":
    print("📈 Cargando datos para visualización...")
    df = pd.read_csv(INPUT_CSV)

    # Estilo general
    sns.set(style="whitegrid")

    # 1. Distribución de etiquetas
    plt.figure(figsize=(6, 4))
    sns.countplot(x="label", data=df, palette="pastel")
    plt.title("Distribución de jugadas buenas (1) y malas (0)")
    plt.xlabel("Etiqueta")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.show()

    # 2. Histogramas de evaluaciones
    for col in ["eval_before", "eval_after", "delta"]:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col], bins=50, kde=True, color="skyblue")
        plt.title(f"Distribución de {col}")
        plt.tight_layout()
        plt.show()

    # 3. Mapa de calor de correlaciones
    plt.figure(figsize=(6, 5))
    corr = df[["eval_before", "eval_after", "delta", "label"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlación entre variables")
    plt.tight_layout()
    plt.show()
