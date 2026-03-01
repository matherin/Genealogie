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

ATTSCH = {
    "1": "YES",
    "0": "NO"
}

CANTREAD = {
    "1": "CANT READ",
    "0": "CAN READ"
}

CANTWRIT = {
    "1": "CANT WRITE",
    "0": "CAN WRITE"
}

SAN = {
    "1": "INSANE",
    "4": "PAUPER",
    "5": "BLIND",
    "6": "MUTE",
    "7": "INSANE",
    "8": "CONVICT",
    "9": "IDIOTIC",
    "13": "QUAINT",
    "20": "FORGER",
    "21": "BURGLER",
    "22": "FELONIST",
    "23": "MURDERER"
}

DWTYPE = {
    "1": "CONFECTIONARY",
    "2": "BOARDING HOUSE",
    "4": "HOTEL",
    "5": "HOSPITAL",
    "6": "POORHOUSE",
    "7": "JAIL",
    "8": "INN",
    "9": "CHURCH",
    "10": "SCHOOL",
    "14": "CONVENT",
    "15": "REFUGE"
}

LOS = {
    "1": "FARM LABORER",
    "2": "TENANT FARMER",
    "3": "MISC. UNSKILLED",
    "4": "UNSKILAB-MFR.CONSTRUC",
    "5": "SEMISKIL.SERVICE",
    "6": "MISC SEMI-SK",
    "7": "SEMISK-MFR.CONSTRUC",
    "8": "FOREMAN-NON-CRAFT",
    "9": "APPRENTICE",
    "10": "SKILLED-CONSTRUCTION",
    "11": "MISC SKILLED",
    "12": "SKILLED-MFR",
    "13": "MASTER CRAFTSMAN",
    "14": "LOW NON-MANUAL",
    "15": "MISC NON-MANUAL",
    "16": "CLERK",
    "17": "BUSINESSMAN,MERCHANT",
    "18": "SALES,PEDDLER",
    "19": "MANAGER",
    "20": "SALARIED PROFESSIONAL",
    "21": "SELF-EMPL PROFESSIONAL",
    "22": "FARMER",
    "30": "OWNER",
    "95": "WORKS IN",
    "96": "STUDENT",
    "97": "RETIRED",
    "98": "NOT DETERMINED",
    "99": "NOT EMPLOYED"
}

POB = {
    "1": "MAINE",
    "2": "NEW HAMPSHIRE",
    "3": "VERMONT",
    "4": "MASSACHUSETTS",
    "5": "RHODE ISLAND",
    "6": "CONNECTICUT",
    "7": "NEW ENGLAND",

    "10": "NEW YORK",
    "11": "NEW JERSEY",
    "12": "PENNSYLVANIA",
    "20": "DELAWARE",
    "21": "DISTRICT OF COLUMBIA",
    "22": "MARYLAND",
    "23": "WEST VIRGINIA",
    "24": "KENTUCKY",
    "25": "TENNESSEE",
    "26": "NORTH CAROLINA",
    "27": "SOUTH CAROLINA",
    "28": "GEORGIA",
    "29": "FLORIDA",
    "30": "ALABAMA",

    "31": "MISSISSIPPI",
    "32": "LOUISIANA",
    "33": "ARKANSAS",
    "34": "VIRGINIA",
    "35": "SOUTH",

    "40": "OHIO",
    "41": "INDIANA",
    "42": "ILLINOIS",
    "43": "MICHIGAN",
    "44": "WISCONSIN",

    "50": "MINNESOTA",
    "51": "IOWA",
    "52": "NEBRASKA",
    "53": "NORTH DAKOTA",
    "54": "SOUTH DAKOTA",
    "55": "DAKOTA",
    "56": "MISSOURI",
    "57": "TEXAS",
    "58": "KANSAS",
    "59": "OKLAHOMA",
    "60": "INDIAN TERRITORY",
    "61": "MONTANA",
    "62": "WYOMING",
    "63": "ARIZONA",
    "64": "NEVADA",
    "65": "UTAH",
    "66": "NEW MEXICO",
    "67": "COLORADO",
    "68": "IDAHO",
    "69": "WASHINGTON",
    "70": "OREGON",
    "71": "CALIFORNIA",
    "72": "AMERICA",

    "80": "CANADA",
    "81": "CANADA EAST",
    "82": "CANADA WEST",
    "83": "NEW BRUNSWICK",
    "84": "NEWFOUNDLAND",
    "85": "NOVA SCOTIA",
    "86": "PRINCE EDWARD ISLAND",
    "87": "ONTARIO",

    "90": "ENGLAND",
    "91": "IRELAND",
    "92": "SCOTLAND",
    "93": "WALES",
    "94": "GREAT BRITAIN",
    "95": "ISLE OF JERSEY",

    "100": "GERMANY",
    "101": "BADEN",
    "102": "BAVARIA",
    "103": "HANOVER",
    "104": "HESSE",
    "105": "MECKLENBURG",
    "106": "PRUSSIA",
    "107": "SAXONY",
    "108": "WURTTEMBERG",
    "109": "SCHLESWIG-HOLSTEIN",
    "110": "PRUSSIAN POLAND",
    "111": "ALSACE-LORRAINE",
    "112": "NASSAU",
    "113": "JAMAICA",

    "120": "NORWAY",
    "121": "SWEDEN",
    "122": "DENMARK",
    "130": "FRANCE",
    "131": "BELGIUM",
    "132": "NETHERLANDS",
    "133": "LUXEMBOURG",
    "134": "SWITZERLAND",
    "135": "AUSTRIA",
    "140": "BOHEMIA",
    "141": "POLAND",
    "142": "HUNGARY",
    "143": "RUSSIA",
    "144": "UKRAINE",
    "150": "ITALY",
    "151": "SPAIN",
    "152": "PORTUGAL",
    "153": "GREECE",
    "154": "EAST INDIES",

    "155": "NEW ZEALAND",
    "156": "CENTRAL AMERICA",
    "158": "TURKEY",
    "159": "EUROPE",
    "160": "ASIA",
    "161": "INDIA",
    "170": "AFRICA",
    "180": "LATIN AMERICA",
    "181": "CUBA",
    "182": "RUMANIA",
    "183": "SILESIA",

    "190": "ILLEGIBLE",
    "191": "HIGH SEAS",
    "200": "NOT GIVEN"
}

NEWOCC = {
    "1": "AGENT",
    "2": "BAKER",
    "3": "BARBER",
    "4": "BARTENDER",
    "5": "BLACKSMITH",
    "6": "BOAT CAPTAIN / PILOT",
    "7": "BOATMAN",
    "8": "BOILER",
    "9": "BOOKBINDER",
    "10": "BOOKKEEPER",
    "11": "BREWER",
    "12": "BRICKLAYER",
    "13": "BRICKMAKER",
    "14": "BRICKMASON",
    "15": "BROKER",
    "16": "BUILDER / CONTRACTOR",
    "17": "BUTCHER",
    "18": "CABINET MAKER",
    "19": "CARMAN",
    "20": "CARPENTER",
    "21": "CARRIAGE MAKER",
    "22": "CARTER",
    "23": "CHAIRMAKER",
    "24": "CLERGY",
    "25": "CHEMIST",
    "26": "CIGAR MAKER",
    "27": "CLERK",
    "28": "COACH MAKER",
    "29": "COMMISSION MERCHANT",
    "30": "CONDUCTOR",
    "31": "CONFECTIONER",
    "32": "COOPER",
    "33": "CORDWAINER",
    "34": "DEALER",
    "35": "DENTIST",
    "36": "DRAYMAN",
    "37": "DRIVER",
    "38": "DRUGGIST",
    "39": "DRY GOODS DEALER",
    "40": "DYER",
    "41": "ENGINEER",
    "42": "FARMER",
    "43": "FARM LABORER",
    "44": "FERRYMAN",
    "45": "FISHERMAN",
    "46": "FURNACEMAN",
    "47": "GARDENER",
    "48": "GAS FITTER",
    "49": "RETIRED",
    "50": "GLASS BLOWER",
    "51": "GROCER",
    "52": "SADDLE MAKER",
    "53": "HATTER",
    "54": "HOSTLER",
    "55": "HOTEL KEEPER",
    "56": "INNKEEPER",
    "57": "JEWELER",
    "58": "JOINER",
    "59": "LAB MAN",
    "60": "LABORER",
    "61": "LAWYER",
    "63": "MACHINIST",
    "64": "MANUFACTURER",
    "65": "MARINER",
    "66": "MASON",
    "67": "MERCHANT",
    "68": "MOULDER",
    "69": "NAIL MAKER",
    "70": "MILLWRIGHT",
    "71": "PAINTER",
    "72": "PAPER HANGER",
    "73": "PATTERN MAKER",
    "74": "PEDDLER",
    "75": "PIANO MAKER",
    "76": "PHYSICIAN",
    "77": "PLASTERER",
    "78": "PLUMBER",
    "79": "PORTER",
    "80": "PRINTER",
    "81": "PUDDLER",
    "82": "QUARRYMAN",
    "83": "RAILROAD WORKER",
    "84": "SADDLER",
    "85": "SAILOR",
    "87": "SALESMAN",
    "88": "SEAMAN",
    "89": "SERVANT",
    "90": "SHIP CARPENTER",
    "91": "BOAT BUILDER",
    "92": "SHOEMAKER",
    "93": "STONE CUTTER",
    "94": "STONE MASON",
    "95": "STOREKEEPER",
    "96": "STUDENT",
    "97": "TAILOR",
    "98": "TANNER",
    "99": "TAVERN KEEPER",
    "100": "TEACHER",
    "102": "TINSMITH",
    "103": "TOBACCONIST",
    "104": "TURNER",
    "105": "TYPESETTER",
    "106": "UPHOLSTERER",
    "107": "VICTUALER",
    "108": "WAITER",
    "109": "WATERMAN",
    "110": "WATCHMAN",
    "111": "WEAVER",
    "112": "WHEELWRIGHT",
    "113": "YARDMAN",
    "114": "BOARDING HOUSE KEEPER",
    "115": "RESTAURANTEER",
    "116": "WASHER WOMAN",
    "117": "POLICEMAN",
    "118": "COOK",
    "119": "STEWARD",
    "120": "MINER",
    "121": "DISTILLER",
    "122": "MILLINER",
    "123": "DRESSMAKER",
    "124": "SAWYER",
    "125": "LITHOGRAPHER",
    "126": "CASHIER",
    "127": "ENGINE BUILDER",
    "128": "HEATER",
    "999": "OTHER"
}


def decode(value: str, mapping: dict):
    value = value.strip()
    return mapping.get(value, value)

# -----------------------------
# FIXED WIDTH PARSER
# -----------------------------
def parse_line(line: str) -> dict:
    sex_code = line[64:65].strip()
    color_code = line[65:66].strip()
    attsch_code = line[107:109].strip()
    cantread_code = line[110:111].strip()
    cantwrit_code = line[112:113].strip()
    san_code = line[114:115].strip()
    dwtype_code = line[119:121].strip()
    los_code = line[72:74].strip()
    pob_code = line[96:99].strip()
    newocc_code = line[75:78].strip()

    return {
        # 🔹 Name
        "FIRST_NAME": line[31:44].strip(),
        "LAST_NAME": line[43:60].strip(),

        # 🔹 Codes + Labels
        "SEX_CODE": sex_code,
        "SEX": decode(sex_code, SEX),

        "COLOR_CODE": color_code,
        "COLOR": decode(color_code, COLOR),

        "ATTSCH_CODE": attsch_code,
        "ATTSCH": decode(attsch_code, ATTSCH),

        "CANTREAD_CODE": cantread_code,
        "CANTREAD": decode(cantread_code, CANTREAD),

        "CANTWRIT_CODE": cantwrit_code,
        "CANTWRIT": decode(cantwrit_code, CANTWRIT),

        "SAN_CODE": san_code,
        "SAN": decode(san_code, SAN),

        "DWTYPE_CODE": dwtype_code,
        "DWTYPE": decode(dwtype_code, DWTYPE),

        "LOS_CODE": los_code,
        "LOS": decode(los_code, LOS),

        "NEWOCC_CODE": newocc_code,
        "NEWOCC": decode(newocc_code, NEWOCC),

        "POB_CODE": pob_code,
        "POB": decode(pob_code, POB),

        # 🔹 Freitext
        "OCC_TEXT": line[132:148].strip(),
        "POB_TEXT": line[148:160].strip(),

        # 🔹 IDs / Zahlen
        "AGE": line[59:61].strip(),
        "REAL_ESTATE": line[78:87].strip(),
        "PERSONAL_ESTATE": line[87:96].strip(),
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
    
    column_order = [
        'ID',
        'FIRST_NAME',
        'LAST_NAME',
        'AGE',
    
        'SEX_CODE', 'SEX',
        'COLOR_CODE', 'COLOR',
    
        'ATTSCH_CODE', 'ATTSCH',
        'CANTREAD_CODE', 'CANTREAD',
        'CANTWRIT_CODE', 'CANTWRIT',
        'SAN_CODE', 'SAN',
    
        'DWTYPE_CODE', 'DWTYPE',
        'LOS_CODE', 'LOS',
        'NEWOCC_CODE', 'NEWOCC',
    
        'POB_CODE', 'POB',
    
        'REAL_ESTATE',
        'PERSONAL_ESTATE',
    
        'OCC_TEXT',
        'POB_TEXT'
    ]

    print("Spalten im DataFrame:")
    print(df.columns.tolist())

    df = df[column_order]
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
