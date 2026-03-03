from .database import db
from .datamodels import Seventy
import os

# -----------------------------
# VALUE LABEL DICTIONARIES
# -----------------------------

SEX = {"1": True, "2": False}

COLOR = {
    "1": "WHITE",
    "2": "BLACK",
    "3": "MULATTO",
    "4": "CHINESE"
}

ATTSCH = {"1": True, "0": False}
CANTREAD = {"1": False, "0": True}
CANTWRIT = {"1": False, "0": True}

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
    "23": "MURDERER",
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
    "15": "REFUGE",
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
    "2": "N. HAMP",
    "3": "VERMONT",
    "4": "MASS",
    "5": "RHODE IS.",
    "6": "CONN.",
    "7": "NEW ENGLAND",

    "10": "N.Y.",
    "11": "N.J.",
    "12": "PENN.",
    "20": "DELAWARE",
    "21": "D.C.",
    "22": "MD.",
    "23": "W. VA.",
    "24": "KY.",
    "25": "TENN",
    "26": "N.C.",
    "27": "S.C.",
    "28": "GA.",
    "29": "FLA",
    "30": "ALA",

    "31": "MISS",
    "32": "LA.",
    "33": "ARK.",
    "34": "VA.",
    "35": "SOUTH",

    "40": "OHIO",
    "41": "IND.",
    "42": "ILL.",
    "43": "MICH.",
    "44": "WISC.",

    "50": "MINN.",
    "51": "IOWA",
    "52": "NEB.",
    "53": "N.DAKOTA",
    "54": "S.DAKOTA",
    "55": "DAKOTA",
    "56": "MISSOURI",
    "57": "TEXAS",
    "58": "KANSAS",
    "59": "OKLAHOMA",
    "60": "INDIAN TERR",
    "61": "MONTANA",
    "62": "WYO.",
    "63": "ARIZ",
    "64": "NEVADA",
    "65": "UTAH",
    "66": "N. MEXICO",
    "67": "COLORADO",
    "68": "IDAHO",
    "69": "WASHINGTON",
    "70": "OREGON",
    "71": "CALIFORNIA",
    "72": "AMERICA",

    "80": "CANADA",
    "81": "CANADA E.",
    "82": "CANADA W.",
    "83": "N. BRUNSWICK",
    "84": "N.FOUNDLAND",
    "85": "NOVA SCOTIA",
    "86": "PRINCE ED IS",
    "87": "CAN.ONTARIO",

    "90": "ENGLAND",
    "91": "IRELAND",
    "92": "SCOTLAND",
    "93": "WALES",
    "94": "GT. BRIT.",
    "95": "IS OF JERSEY",

    "100": "GERMANY",
    "101": "BADEN",
    "102": "BAVARIA",
    "103": "HANOVER",
    "104": "HESSE",
    "105": "MECKLENBURG",
    "106": "PRUSSIA",
    "107": "SAXONY",
    "108": "WERTENBURG",
    "109": "SCHLESWIG-HOLSTEIN",
    "110": "PRUSSIAN POLAND",
    "111": "ALSACE-LORRAINE",
    "112": "NASUA",
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
    "154": "E. INDIES",

    "155": "N. ZEALAND",
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
    "6": "BOAT CAPTAIN-PILOT",
    "7": "BOATMAN",
    "8": "BOILER",
    "9": "BOOKBINDER",
    "10": "BOOKKEEPER",
    "11": "BREWER",
    "12": "BRICKLAYER",
    "13": "BRICKMAKER",
    "14": "BRICKMASON",
    "15": "BROKER",
    "16": "BUILDER.CONTRACTOR",
    "17": "BUTCHER",
    "18": "CABMAKER",
    "19": "CARMAN",
    "20": "CARPENTER",
    "21": "CARRIAGEMAKER",
    "22": "CARTER",
    "23": "CHAIRMAKER",
    "24": "CLERGY",
    "25": "CHEMIST",
    "26": "CIGARMAKER",
    "27": "CLERK",
    "28": "COACHMAKER",
    "29": "COMMISSION MRCHT",
    "30": "CONDUCTOR",
    "31": "CONFECTIONER",
    "32": "COOPER",
    "33": "CORDWAINER",
    "34": "DEALER",
    "35": "DENTIST",
    "36": "DRAYMAN",
    "37": "DRIVER",
    "38": "DRUGGIST",
    "39": "DRY GOODS",
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
    "69": "NAILMAKER",
    "70": "MILLWRIGHT",
    "71": "PAINTER",
    "72": "PAPER HANGER",
    "73": "PATTERNMAKER",
    "74": "PEDDLER",
    "75": "PIANOMAKER",
    "76": "PHYSICIAN",
    "77": "PLASTERER",
    "78": "PLUMBER",
    "79": "PORTER",
    "80": "PRINTER",
    "81": "PUDDLER",
    "82": "QUARRYMAN",
    "83": "RR WORKER",
    "84": "SADDLER",
    "85": "SAILOR",
    "87": "SALESMAN",
    "88": "SEAMAN",
    "89": "SERVANT",
    "90": "SHIPCARPENTER",
    "91": "BOAT BUILDER",
    "92": "SHOEMAKER",
    "93": "STONECUTTER",
    "94": "STONEMASON",
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
    "114": "BOARDINGHOUSE",
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


# -----------------------------
# HELPERS
# -----------------------------

def decode(value: str, mapping: dict):
    value = value.strip()
    return mapping.get(value)


def to_int(value):
    try:
        return int(value.strip())
    except:
        return None


# -----------------------------
# FIXED WIDTH PARSER
# -----------------------------

def parse_line(line: str):

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
    ffb_code=line[100:101].strip()
    mfb_code=line[102:103].strip()
    can_vote_code=line[116:117].strip()


    first_name = line[31:44].strip()
    last_name = line[43:59].strip()
    ward_number = to_int(line[9:11])

    month_born=line[103:105].strip()
    month_married=line[105:107].strip()

    age = to_int(line[59:61])

    real_estate = to_int(line[78:87])
    personal_estate = to_int(line[87:96])

    occ_text = line[132:148].strip()
    pob_text = line[148:160].strip()

    return Seventy(

        first_name=first_name,
        alt_first_name=None,

        last_name=last_name,
        alt_last_name=None,

        age=age,

        month_born=month_born,
        male=decode(sex_code, SEX),

        month_married=month_married,

        color=decode(color_code, COLOR),

        occupation=decode(newocc_code, NEWOCC) or occ_text,

        level_of_skill=decode(los_code, LOS),

        ward_number=ward_number,

        place_of_birth=decode(pob_code, POB) or pob_text,

        ffb=decode(ffb_code, ATTSCH),
        mfb=decode(mfb_code, ATTSCH),

        a_school=decode(attsch_code, ATTSCH),

        read=decode(cantread_code, CANTREAD),
        write=decode(cantwrit_code, CANTWRIT),

        dwelling=decode(dwtype_code, DWTYPE),

        personal_estate=personal_estate,
        real_estate=real_estate,

        vote=decode(can_vote_code, ATTSCH),

        sane=decode(san_code, SAN),

        soundex_code=None,
        alt_soundex_code=None,

        notes=None
    )


# -----------------------------
# SEED DATABASE
# -----------------------------

def seed_database():

    if Seventy.query.first():
        print("Database already seeded.")
        return

    print("Seeding database...")

    records = []

    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "..", "data", "input.txt")
    file_path = os.path.normpath(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                person = parse_line(line)
                records.append(person)

    db.session.bulk_save_objects(records)
    db.session.commit()

    print(f"Inserted {len(records)} records.")