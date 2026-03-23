sentences = [
    "AI is amazing.",
    "Artificial Intelligence is amazing.",
    "AI is 🔥."
]
 
for s in sentences:
    t = enc.encode(s)
    print(f"Text: {s}\nTokens: {len(t)} → {t}\n")
