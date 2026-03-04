from .database import db
from .datamodels import *
import os

# VALUE LABEL DICTIONARIES

SEX = {"1": True, "2": False}

COLOR = {
    "1": "WHITE",
    "2": "BLACK",
    "3": "MULATTO",
    "4": "CHINESE"
}

MARSTAT = {
    "1": "SINGLE",
    "2": "MARRIED",
    "3": "DIVORCED",
    "4": "WIDOWED"
}

HHREL_MAP = {
    "1": "HEAD",
    "2": "SPOUSE",
    "3": "SIBLING",
    "4": "SON/DAUGHTER",
    "5": "PARENT",
    "6": "GRANDPARENT",
    "8": "STEP-PARENT",
    "11": "HALF-SIBLING",
    "12": "UNCLE/AUNT",
    "13": "COUSIN",
    "14": "NIECE/NEPHEW",
    "15": "GRANDCHILD",
    "17": "ADOPTED CHILD",
    "18": "STEP-CHILD",
    "19": "PARENT-IN-LAW",
    "20": "SIBLING-IN-LAW",
    "21": "SON/DAU-IN-LAW",
    "27": "2ND COUSIN",
    "28": "BOARDER",
    "29": "ROOMER",
    "31": "SERVANT",
    "32": "EMPLOYEE",
    "33": "VISITOR/FRIEND",
    "36": "ORPHAN",
    "38": "PATIENT",
    "39": "NUN",
    "41": "TEACHER",
    "43": "NURSE",
    "48": "COACHMAN",
    "51": "PARTNER",
    "52": "ASSISTANT/COMPANION",
    "53": "AUNT/NEPHEW-IN-LAW",
    "55": "INMATE",
    "84": "GRAND-NEPHEW"
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

# HELPERS

def decode(value: str, mapping: dict):
    value = value.strip()
    return mapping.get(value)


def to_int(value):
    try:
        return int(value.strip())
    except:
        return None

# FIXED WIDTH PARSER

def parse_line(line):

    wardNumber = to_int(line[6:8])

    lastName = line[34:49].strip()
    firstName = line[25:33].strip()

    age = to_int(line[49:51])

    sex = line[54:55].strip()
    color = line[55:56].strip()
    occupation = line[105:117].strip()
    skillLevel = line[62:64].strip()

    rthoh = line[73:75].strip()

    maritalStatus = line[75:76].strip()
    monthsUnemployed = to_int(line[76:78])

    placeOfBirth = line[117:127].strip()
    pobFather = line[127:135].strip()
    pobMother = line[135:142].strip()

    street = line[142:153].strip()
    houseAddress = line[68:73].strip()

    return Eighty(
        firstName=firstName,
        lastName=lastName,
        age=age,
        rthoh=decode(rthoh, HHREL_MAP),
        sex=decode(sex, SEX),
        color=decode(color, COLOR),
        occupation=decode(occupation, NEWOCC) or occupation,
        skillLevel=decode(skillLevel, LOS),
        wardNumber=wardNumber,
        placeOfBirth=decode(placeOfBirth, POB) or placeOfBirth,
        pobFather=pobFather,
        pobMother=pobMother,
        street=street,
        houseAddress=None,
        monthsUnemployed=monthsUnemployed,
        maritalStatus=decode(maritalStatus, MARSTAT)
    )

# SEED DATABASE

def seed_eighty_database():

    if Eighty.query.first():
        print("Database already seeded.")
        return

    print("Seeding database with the data of eighty...")

    records = []

    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "..", "data", "eighty.txt")
    file_path = os.path.normpath(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                person = parse_line(line)
                records.append(person)

    db.session.bulk_save_objects(records)
    db.session.commit()

    print(f"Inserted {len(records)} records.")