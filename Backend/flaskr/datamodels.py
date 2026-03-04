from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from . import db

class Seventy(db.Model):
    __tablename__ = "seventy"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    alternateFirstName = Column(String(255))
    lastName = Column(String(255))
    alternateLastName = Column(String(255))
    age = Column(Integer)
    monthBorn = Column(String(255))
    sex = Column(Boolean)
    monthMarried = Column(String(255))
    color = Column(String(255))
    occupation = Column(String(255))
    skillLevel = Column(String(255))
    wardNumber = Column(Integer)
    placeOfBirth = Column(String(255))
    fatherForeignBorn = Column(Boolean)
    motherForeignBorn = Column(Boolean)
    attendSchool = Column(Boolean)
    read = Column(Boolean)
    write = Column(Boolean)
    dwelling = Column(String(255))
    personalEstate = Column(Integer)
    realEstate = Column(Integer)
    vote = Column(Boolean)
    sane = Column(String(255))
    soundexCode = Column(String(255))
    alternateSoundexCode = Column(String(255))
    addNotes = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "firstName": self.firstName,
            "alternateFirstName": self.alternateFirstName,
            "lastName": self.lastName,
            "alternateLastName": self.alternateLastName,
            "age": self.age,
            "monthBorn": self.monthBorn,
            "sex": self.sex,
            "monthMarried": self.monthMarried,
            "color": self.color,
            "occupation": self.occupation,
            "skillLevel": self.skillLevel,
            "wardNumber": self.wardNumber,
            "placeOfBirth": self.placeOfBirth,
            "fatherForeignBorn": self.fatherForeignBorn,
            "motherForeignBorn": self.motherForeignBorn,
            "attendSchool": self.attendSchool,
            "read": self.read,
            "write": self.write,
            "dwelling": self.dwelling,
            "personalEstate": self.personalEstate,
            "realEstate": self.realEstate,
            "vote": self.vote,
            "sane": self.sane,
            "soundexCode": self.soundexCode,
            "alternateSoundexCode": self.alternateSoundexCode,
            "addNotes": self.addNotes
        }
        return data
    
    def __repr__(self):
        return f"<seventy(id={self.id}, firstName={self.firstName}, lastName={self.lastName})>"

class Eighty(db.Model):
    __tablename__ = "eighty"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    lastName = Column(String(255))
    rthoh = Column(String(255))
    age = Column(Integer)
    sex = Column(Boolean)
    marital_status = Column(String(255))
    color = Column(String(255))
    occupation = Column(String(255))
    skillLevel = Column(String(255))
    wardNumber = Column(Integer)
    months_unemployed = Column(Integer)
    placeOfBirth = Column(String(255))
    pob_father = Column(String(255))
    pob_mother = Column(String(255))
    street = Column(String(255))
    house_address = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "rthoh": self.rthoh,
            "age": self.age,
            "sex": self.sex,
            "marital_status": self.marital_status,
            "color": self.color,
            "occupation": self.occupation,
            "skillLevel": self.skillLevel,
            "wardNumber": self.wardNumber,
            "months_unemployed": self.months_unemployed,
            "placeOfBirth": self.placeOfBirth,
            "pob_father": self.pob_father,
            "pob_mother": self.pob_mother,
            "street": self.street
        }
        return data
    
    def __repr__(self):
        return f"<eighty(id={self.id}, firstName={self.firstName}, lastName={self.lastName})>"


class Sixty(db.Model):
    __tablename__ = "sixty"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    alternateFirstName = Column(String(255))
    lastName = Column(String(255))
    alternateLastName = Column(String(255))
    age = Column(Integer)
    sex = Column(Boolean)
    married_last_year = Column(Boolean)
    color = Column(String(255))
    occupation = Column(String(255))
    skillLevel = Column(String(255))
    wardNumber = Column(Integer)
    placeOfBirth = Column(String(255))
    attendSchool = Column(Boolean)
    literate = Column(Boolean)
    dwelling = Column(String(255))
    personalEstate = Column(Integer)
    realEstate = Column(Integer)
    sane = Column(String(255))
    soundexCode = Column(String(255))
    alternateSoundexCode = Column(String(255))
    addNotes = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "firstName": self.firstName,
            "alternateFirstName": self.alternateFirstName,
            "lastName": self.lastName,
            "alternateLastName": self.alternateLastName,
            "age": self.age,
            "sex": self.sex,
            "married_last_year": self.married_last_year,
            "color": self.color,
            "occupation": self.occupation,
            "skillLevel": self.skillLevel,
            "wardNumber": self.wardNumber,
            "placeOfBirth": self.placeOfBirth,
            "attendSchool": self.attendSchool,
            "literate": self.literate,
            "dwelling": self.dwelling,
            "personalEstate": self.personalEstate,
            "realEstate": self.realEstate,
            "sane": self.sane,
            "soundexCode": self.soundexCode,
            "alternateSoundexCode": self.alternateSoundexCode,
            "addNotes": self.addNotes
        }
        return data
    
    def __repr__(self):
        return f"<sixty(id={self.id}, firstName={self.firstName}, lastName={self.lastName})>"
    

class Fifty(db.Model):
    __tablename__ = "fifty"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    alternateFirstName = Column(String(255))
    lastName = Column(String(255))
    alternateLastName = Column(String(255))
    age = Column(Integer)
    sex = Column(Boolean)
    married_last_year = Column(Boolean)
    color = Column(String(255))
    occupation = Column(String(255))
    skillLevel = Column(String(255))
    wardNumber = Column(Integer)
    placeOfBirth = Column(String(255))
    attendSchool = Column(Boolean)
    literate = Column(Boolean)
    dwelling = Column(String(255))
    estate_value = Column(Integer)
    sane = Column(String(255))
    soundexCode = Column(String(255))
    alternateSoundexCode = Column(String(255))
    addNotes = Column(String(255))

    def to_dict(self, include_id=True):
        data = {
            "id": self.id if include_id else None,
            "firstName": self.firstName,
            "alternateFirstName": self.alternateFirstName,
            "lastName": self.lastName,
            "alternateLastName": self.alternateLastName,
            "age": self.age,
            "sex": self.sex,
            "married_last_year": self.married_last_year,
            "color": self.color,
            "occupation": self.occupation,
            "skillLevel": self.skillLevel,
            "wardNumber": self.wardNumber,
            "placeOfBirth": self.placeOfBirth,
            "attendSchool": self.attendSchool,
            "literate": self.literate,
            "dwelling": self.dwelling,
            "estate_value": self.estate_value,
            "sane": self.sane,
            "soundexCode": self.soundexCode,
            "alternateSoundexCode": self.alternateSoundexCode,
            "addNotes": self.addNotes
        }
        return data
    
    def __repr__(self):
        return f"<fifty(id={self.id}, firstName={self.firstName}, lastName={self.lastName})>"