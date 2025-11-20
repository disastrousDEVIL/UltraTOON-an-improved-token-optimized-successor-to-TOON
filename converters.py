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

def json_to_ultra_toon(data: dict):
    """
    Ultra compressed TOON using:
    - Single-letter column names
    - Schema legend

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

    # Legend block
    legend = "SCHEMA: " + "; ".join(f"{short[c]}={c}" for c in columns)

    # Ultra header
    header = f"{key[0]}[{len(rows)}]{{{','.join(short[c] for c in columns)}}}:"

    # Body with rows
    body = ""
    for r in rows:
        line = ",".join(str(r[c]) for c in columns)
        body += f"\n  {line}"

    return legend + "\n" + header + body