import pandas as pd
import chess
import chess.engine
from tqdm import tqdm

# Ruta al ejecutable de Stockfish (ajústalo a tu sistema)
STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"  # o "C:/ruta/stockfish.exe" en Windows

# Archivo de entrada y salida
INPUT_CSV = "Classifier-of-good-or-bad-plays/Data/parsed_moves.csv"
OUTPUT_CSV = "Classifier-of-good-or-bad-plays/Data/evaluated_moves.csv"


# Cantidad de registros a evaluar (limite inicial)
EVAL_LIMIT = 20000

# Umbral para etiquetar jugadas malas (en centipawns)
BAD_MOVE_THRESHOLD = -100  # -1.00

def centipawn_score(info):
    if info.get("score") is None:
        return 0
    score = info["score"].white()
    return score.score(mate_score=10000) if score is not None else 0

def evaluate_positions():
    df = pd.read_csv(INPUT_CSV).head(EVAL_LIMIT)
    evals = []

    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Evaluando jugadas"):
        try:
            board = chess.Board(row["fen"])
            move = board.parse_san(row["move"])

            # Evaluación antes de la jugada
            info_before = engine.analyse(board, chess.engine.Limit(depth=12))
            eval_before = centipawn_score(info_before)

            # Aplicar la jugada
            board.push(move)

            # Evaluación después de la jugada
            info_after = engine.analyse(board, chess.engine.Limit(depth=12))
            eval_after = centipawn_score(info_after)

            delta = eval_after - eval_before
            label = 0 if delta < BAD_MOVE_THRESHOLD else 1

            evals.append({
                "fen": row["fen"],
                "move": row["move"],
                "eval_before": eval_before,
                "eval_after": eval_after,
                "delta": delta,
                "label": label
            })

        except Exception as e:
            # Si hay algún error (por jugada ilegal, FEN inválida, etc), lo saltamos
            continue

    engine.quit()
    return pd.DataFrame(evals)

if __name__ == "__main__":
    print(f"🔍 Evaluando primeras {EVAL_LIMIT} jugadas con Stockfish...")
    df_eval = evaluate_positions()
    df_eval.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Evaluación completada. Guardado en {OUTPUT_CSV}")
    print(f"Total de jugadas evaluadas exitosamente: {len(df_eval)}")