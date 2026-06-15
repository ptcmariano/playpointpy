#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path

from faster_whisper import WhisperModel
from rapidfuzz import fuzz
from unidecode import unidecode


# ============================================================
# CONFIGURAÇÕES
# ============================================================

WHISPER_MODEL = "large-v3"
MATCH_THRESHOLD = 80

# ============================================================
# UTILITÁRIOS
# ============================================================

def normalize(text: str) -> str:
    """
    Remove acentos, pontuação e converte para minúsculo.
    """
    text = unidecode(text.lower())

    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"\([^)]*\)", " ", text)

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_lyrics(filepath):
    """
    Carrega a letra oficial.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


# ============================================================
# TRANSCRIÇÃO
# ============================================================

def transcribe(mp3_path):
    """
    Gera timestamps no nível da palavra.
    """

    print("Carregando Whisper...")

    model = WhisperModel(
        WHISPER_MODEL,
        device="cpu",
        compute_type="int8"
    )

    print("Transcrevendo áudio...")

    segments, info = model.transcribe(
        mp3_path,
        beam_size=5,
        word_timestamps=True
    )

    words = []

    for segment in segments:
        if not segment.words:
            continue

        for word in segment.words:
            token = normalize(word.word)

            if token:
                words.append({
                    "word": token,
                    "start": word.start,
                    "end": word.end
                })

    return words


# ============================================================
# MATCHING
# ============================================================

def find_best_match(target_words, transcript_words):
    """
    Procura o melhor trecho da transcrição
    para uma frase da letra oficial.
    """

    target_text = " ".join(target_words)

    best_score = -1
    best_start = None

    n = len(target_words)

    for i in range(len(transcript_words) - n + 1):

        candidate = transcript_words[i:i+n]

        candidate_text = " ".join(
            w["word"] for w in candidate
        )

        score = fuzz.ratio(
            target_text,
            candidate_text
        )

        if score > best_score:
            best_score = score
            best_start = i

    if best_score < MATCH_THRESHOLD:
        return None

    return {
        "score": best_score,
        "start_index": best_start,
        "start_time": transcript_words[best_start]["start"]
    }


# ============================================================
# MAPEAMENTO
# ============================================================

def map_lyrics(lyrics_lines, transcript_words):

    results = []

    for line in lyrics_lines:

        clean_line = normalize(line)

        if not clean_line:
            continue

        words = clean_line.split()

        match = find_best_match(
            words,
            transcript_words
        )

        if not match:
            results.append({
                "text": line,
                "timestamp": None,
                "confidence": 0
            })
            continue

        results.append({
            "text": line,
            "timestamp": round(match["start_time"], 3),
            "confidence": round(match["score"], 2)
        })

    return results


# ============================================================
# EXPORTAÇÃO
# ============================================================

def save_json(data, output_file):

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


# ============================================================
# MAIN
# ============================================================

def main():

    if len(sys.argv) != 4:
        print(
            "Uso:\n"
            "python transcript-map.py audio.mp3 letra.txt output.json"
        )
        sys.exit(1)

    mp3_file = sys.argv[1]
    lyrics_file = sys.argv[2]
    output_file = sys.argv[3]

    lyrics = load_lyrics(lyrics_file)

    transcript_words = transcribe(mp3_file)

    mapped = map_lyrics(
        lyrics,
        transcript_words
    )

    save_json(mapped, output_file)

    print(f"Arquivo salvo: {output_file}")


if __name__ == "__main__":
    main()