import chess.pgn
import pandas as pd
from tqdm import tqdm

# This script extracts FENs and moves from a PGN file and saves them to a CSV file.
# It processes a specified number of games and outputs the results in a structured format.

PGN_PATH = "Classifier-of-good-or-bad-plays/Data/lichess_db_standard_rated_2014-01.pgn"
OUTPUT_CSV = "Classifier-of-good-or-bad-plays/Data/parsed_moves.csv"


MAX_GAMES = 10000

def extract_fens_and_moves(pgn_path, max_games):
    data = []
    with open(pgn_path, encoding="utf-8") as pgn:
        for game_number in tqdm(range(max_games), desc="Procesando partidas"):
            game = chess.pgn.read_game(pgn)
            if game is None:
                break  # fin del archivo

            board = game.board()
            for move in game.mainline_moves():
                fen_before = board.fen()
                move_san = board.san(move)
                board.push(move)

                data.append({
                    "fen": fen_before,
                    "move": move_san
                })

    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Extrayendo jugadas y FENs desde el archivo PGN...")
    df = extract_fens_and_moves(PGN_PATH, MAX_GAMES)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Extracción completada. Jugadas guardadas en: {OUTPUT_CSV}")
    print(f"Total de registros: {len(df)}")

