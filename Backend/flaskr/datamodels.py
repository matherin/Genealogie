from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from . import db

class Seventy(db.Model):
    __tablename__ = "seventy"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    alt_first_name = Column(String(255))
    last_name = Column(String(255))
    alt_last_name = Column(String(255))
    age = Column(Integer)
    month_born = Column(String(255))
    male = Column(Boolean)
    month_married = Column(String(255))
    color = Column(String(255))
    occupation = Column(String(255))
    level_of_skill = Column(String(255))
    ward_number = Column(Integer)
    place_of_birth = Column(String(255))
    ffb = Column(Boolean)
    mfb = Column(Boolean)
    a_school = Column(Boolean)
    read = Column(Boolean)
    write = Column(Boolean)
    dwelling = Column(String(255))
    personal_estate = Column(Integer)
    real_estate = Column(Integer)
    vote = Column(Boolean)
    sane = Column(String(255))
    soundex_code = Column(String(255))
    alt_soundex_code = Column(String(255))
    notes = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "first_name": self.first_name,
            "alt_first_name": self.alt_first_name,
            "last_name": self.last_name,
            "alt_last_name": self.alt_last_name,
            "age": self.age,
            "month_born": self.month_born,
            "male": self.male,
            "month_married": self.month_married,
            "color": self.color,
            "occupation": self.occupation,
            "level_of_skill": self.level_of_skill,
            "ward_number": self.ward_number,
            "place_of_birth": self.place_of_birth,
            "ffb": self.ffb,
            "mfb": self.mfb,
            "a_school": self.a_school,
            "read": self.read,
            "write": self.write,
            "dwelling": self.dwelling,
            "personal_estate": self.personal_estate,
            "real_estate": self.real_estate,
            "vote": self.vote,
            "sane": self.sane,
            "soundex_code": self.soundex_code,
            "alt_soundex_code": self.alt_soundex_code,
            "notes": self.notes
        }
        return data
    
    def __repr__(self):
        return f"<seventy(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"

class Eighty(db.Model):
    __tablename__ = "eighty"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    rthoh = Column(String(255))
    age = Column(Integer)
    male = Column(Boolean)
    marital_status = Column(String(255))
    color = Column(String(255))
    occupation = Column(String(255))
    level_of_skill = Column(String(255))
    ward_number = Column(Integer)
    months_unemployed = Column(Integer)
    place_of_birth = Column(String(255))
    pob_farther = Column(String(255))
    pob_mother = Column(String(255))
    street = Column(String(255))
    house_address = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rthoh": self.rthoh,
            "age": self.age,
            "male": self.male,
            "marital_status": self.marital_status,
            "color": self.color,
            "occupation": self.occupation,
            "level_of_skill": self.level_of_skill,
            "ward_number": self.ward_number,
            "months_unemployed": self.months_unemployed,
            "place_of_birth": self.place_of_birth,
            "pob_farther": self.pob_farther,
            "pob_mother": self.pob_mother,
            "street": self.street,
            "house_address": self.house_address
        }
        return data
    
    def __repr__(self):
        return f"<eighty(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"


class Sixty(db.Model):
    __tablename__ = "sixty"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    alt_first_name = Column(String(255))
    last_name = Column(String(255))
    alt_last_name = Column(String(255))
    age = Column(Integer)
    male = Column(Boolean)
    married_last_year = Column(Boolean)
    color = Column(String(255))
    occupation = Column(String(255))
    level_of_skill = Column(String(255))
    ward_number = Column(Integer)
    place_of_birth = Column(String(255))
    a_school = Column(Boolean)
    literate = Column(Boolean)
    dwelling = Column(String(255))
    personal_estate = Column(Integer)
    real_estate = Column(Integer)
    sane = Column(String(255))
    soundex_code = Column(String(255))
    alt_soundex_code = Column(String(255))
    notes = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "first_name": self.first_name,
            "alt_first_name": self.alt_first_name,
            "last_name": self.last_name,
            "alt_last_name": self.alt_last_name,
            "age": self.age,
            "male": self.male,
            "married_last_year": self.married_last_year,
            "color": self.color,
            "occupation": self.occupation,
            "level_of_skill": self.level_of_skill,
            "ward_number": self.ward_number,
            "place_of_birth": self.place_of_birth,
            "a_school": self.a_school,
            "literate": self.literate,
            "dwelling": self.dwelling,
            "personal_estate": self.personal_estate,
            "real_estate": self.real_estate,
            "sane": self.sane,
            "soundex_code": self.soundex_code,
            "alt_soundex_code": self.alt_soundex_code,
            "notes": self.notes
        }
        return data
    
    def __repr__(self):
        return f"<sixty(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"
    

class Fifty(db.Model):
    __tablename__ = "fifty"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    alt_first_name = Column(String(255))
    last_name = Column(String(255))
    alt_last_name = Column(String(255))
    age = Column(Integer)
    male = Column(Boolean)
    married_last_year = Column(Boolean)
    color = Column(String(255))
    occupation = Column(String(255))
    level_of_skill = Column(String(255))
    ward_number = Column(Integer)
    place_of_birth = Column(String(255))
    a_school = Column(Boolean)
    literate = Column(Boolean)
    dwelling = Column(String(255))
    estate_value = Column(Integer)
    sane = Column(String(255))
    soundex_code = Column(String(255))
    alt_soundex_code = Column(String(255))
    notes = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "first_name": self.first_name,
            "alt_first_name": self.alt_first_name,
            "last_name": self.last_name,
            "alt_last_name": self.alt_last_name,
            "age": self.age,
            "male": self.male,
            "married_last_year": self.married_last_year,
            "color": self.color,
            "occupation": self.occupation,
            "level_of_skill": self.level_of_skill,
            "ward_number": self.ward_number,
            "place_of_birth": self.place_of_birth,
            "a_school": self.a_school,
            "literate": self.literate,
            "dwelling": self.dwelling,
            "estate_value": self.estate_value,
            "sane": self.sane,
            "soundex_code": self.soundex_code,
            "alt_soundex_code": self.alt_soundex_code,
            "notes": self.notes
        }
        return data
    
    def __repr__(self):
        return f"<fifty(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"