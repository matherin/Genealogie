import pandas as pd

# -----------------------------
# VALUE LABEL DICTIONARIES
# (gekürzt – leicht erweiterbar)
# -----------------------------
SEX = {
    "1": "MALE",
    "2": "FEMALE"
}

COLOR = {
    "1": "WHITE",
    "2": "BLACK",
    "3": "MULATTO",
    "4": "CHINESE"
}

POB = {
    "12": "PENNSYLVANIA",
    "90": "ENGLAND",
    "91": "IRELAND",
    "100": "GERMANY",
    "152": "PORTUGAL"
}

NEWOCC = {
    "90": "SHIP CARPENTER",
    "43": "FARM LABORER",
    "96": "STUDENT"
}

# -----------------------------
# FIXED WIDTH PARSER
# -----------------------------
def parse_line(line: str) -> dict:
    return {
        "YEAR": line[0:2].strip(),
        "TOWN": line[7:9].strip(),
        "WARD": line[9:11].strip(),
        "DWELLING": line[21:26].strip(),
        "HOUSEHOLD": line[26:31].strip(),

        "AGE": line[59:61].strip(),
        "SEX": SEX.get(line[64:65].strip(), line[64:65].strip()),
        "COLOR": COLOR.get(line[65:66].strip(), line[65:66].strip()),

        "OCC_CODE": line[66:72].strip(),
        "LOS": line[72:74].strip(),
        "NEWOCC": NEWOCC.get(line[75:78].strip(), line[75:78].strip()),

        "REAL_ESTATE": line[78:87].strip(),
        "PERSONAL_ESTATE": line[87:96].strip(),

        "POB_CODE": line[96:99].strip(),
        "POB": POB.get(line[96:99].strip(), line[96:99].strip()),

        "OCC_TEXT": line[132:148].strip(),
        "POB_TEXT": line[148:160].strip(),

        "ID": line[126:132].strip()
    }

# -----------------------------
# MAIN CONVERSION
# -----------------------------
def convert_txt_to_excel(input_file, output_file):
    records = []

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                records.append(parse_line(line))

    df = pd.DataFrame(records)
    df.to_excel(output_file, index=False)
    print(f"✅ Fertig: {output_file}")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    convert_txt_to_excel(
        "input.txt",
        "output.xlsx"
    )
