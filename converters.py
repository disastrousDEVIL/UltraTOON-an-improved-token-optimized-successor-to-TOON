from pathlib import Path
def json_to_toon(data: dict):
    """
    Convert a flat JSON list into pure TOON format.

    Example:
    {
      "users": [
        {"id":1, "name":"Alice"},
        {"id":2, "name":"Bob"}
      ]
    }

    → 

    users[2]{id,name}:
      1,Alice
      2,Bob
    """

    key=list(data.keys())[0]
    rows=data[key]

    columns=list(rows[0].keys())

    toon = f"{key}[{len(rows)}]{{{','.join(columns)}}}:\n"

    for r in rows:
        line = ",".join(str(r[c]) for c in columns)
        toon += f"  {line}\n"

    return toon

def json_to_ultra_toon(
    data: dict,
    value_encodings: dict | None = None,
    auto_encode_fields: list[str] | None = None,
):
    """
    Ultra compressed TOON using:
    - Single-letter column names
    - Schema legend
    - Optional single-letter label encoding for categorical values

    Example:

    SCHEMA: i=id; n=name
    u[2]{i,n}:
      1,Alice
      2,Bob
    """
    key = list(data.keys())[0]
    rows = data[key]

    columns = list(rows[0].keys())

    # One-letter column aliases
    short = {c: c[0] for c in columns}

    # Detect which fields to auto-encode if not explicitly provided
    if auto_encode_fields is None:
        # Heuristic: string-typed columns with a small set of distinct values
        auto_encode_fields = []
        for c in columns:
            values = [r.get(c) for r in rows]
            if all(isinstance(v, str) for v in values):
                uniq = {v for v in values}
                if 1 < len(uniq) <= 16:
                    auto_encode_fields.append(c)

    # Build value encodings per field
    value_encodings = value_encodings or {}

    def build_single_letter_codes(categories: list[str]) -> dict[str, str]:
        # Prefer unique letters from within the word; fall back to any unused letter
        assigned: dict[str, str] = {}
        used_letters: set[str] = set()

        # Attempt first-choice letters (first char)
        for cat in categories:
            letter = None
            for ch in cat.lower():
                if ch.isalpha() and ch not in used_letters:
                    letter = ch
                    break
            if letter is None:
                # fallback pool
                for ch in "abcdefghijklmnopqrstuvwxyz":
                    if ch not in used_letters:
                        letter = ch
                        break
            assigned[cat] = letter  # type: ignore
            used_letters.add(letter)  # type: ignore
        return {k: v for k, v in assigned.items()}

    # Create mappings for fields needing encoding and not already provided
    encode_maps: dict[str, dict[str, str]] = {}
    for field in auto_encode_fields:
        # If explicit mapping supplied, use it
        if field in value_encodings:
            encode_maps[field] = value_encodings[field]
            continue
        # Otherwise auto-generate
        cats = sorted({str(r[field]) for r in rows})
        encode_maps[field] = build_single_letter_codes(cats)

    # Ultra header
    header = f"{key[0]}[{len(rows)}]{{{','.join(short[c] for c in columns)}}}:"

    # Body with rows
    body = ""
    for r in rows:
        encoded_values = []
        for c in columns:
            if c in encode_maps:
                original = str(r[c])
                code = encode_maps[c].get(original, original)
                encoded_values.append(str(code))
            else:
                encoded_values.append(str(r[c]))
        line = ",".join(encoded_values)
        body += f"\n  {line}"

    # Legend blocks
    legend_schema = "SCHEMA: " + "; ".join(f"{short[c]}={c}" for c in columns)

    # Add ENCODE lines only for columns that were encoded
    legend_encodes = ""
    if encode_maps:
        for field, mapping in encode_maps.items():
            pairs = "; ".join(f"{code}={label}" for label, code in mapping.items())
            legend_encodes += f"\nENCODE {field}: {pairs}"

    legend = legend_schema + legend_encodes

    full_output = legend + "\n" + header + body

    # Also write to a text file next to this module
    output_path = Path(__file__).parent / "ultra_toon_output.txt"
    with output_path.open("w", encoding="utf-8") as f:
        f.write(full_output + "\n")

    return full_output