CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(255) NOT NULL,
  "role" VARCHAR(255),
  "password" VARCHAR(255) NOT NULL
);

CREATE TABLE "Adressen" (
  "AdresseID" SERIAL PRIMARY KEY,
  "Strasse" VARCHAR(255) NOT NULL,
  "Hausnummer" VARCHAR(10) NOT NULL,
  "Postleitzahl" VARCHAR(10) NOT NULL,
  "Ort" VARCHAR(100) NOT NULL,
  "Land" VARCHAR(100) NOT NULL
);

CREATE TABLE "Kunden" (
  "KID" SERIAL PRIMARY KEY,
  "Firma" VARCHAR(255),
  "Kontonummer" VARCHAR(50),
  "Steuerummer" VARCHAR(50),
  "Ansprechpartner1" VARCHAR(255) NOT NULL,
  "Ansprechpartner2" VARCHAR(255),
  "Ansprechpartner3" VARCHAR(255),
  "Telefonnummer1" VARCHAR(20),
  "Telefonnummer2" VARCHAR(20),
  "Telefonnummer3" VARCHAR(20),
  "EMail1" VARCHAR(255) NOT NULL,
  "EMail2" VARCHAR(255),
  "EMail3" VARCHAR(255),
  "Lieferadresse_ID" INT NOT NULL,
  "Rechnungsadresse_ID" INT NOT NULL,
  "privat" BOOLEAN,
  "Anmerkungen" text
);

CREATE TABLE "Vertraege" (
  "VID" SERIAL PRIMARY KEY,
  "KID" INT NOT NULL,
  "MwSt" DECIMAL(5,2),
  "Datum" timestamp,
  "Annahme" BOOLEAN
);

CREATE TABLE "Waren" (
  "WID" SERIAL PRIMARY KEY,
  "Bezeichnung" VARCHAR(255),
  "Preis" DECIMAL(10,2),
  "Einheit" VARCHAR(50),
  "Abfallschlüsselnummer" VARCHAR(250),
  "Sammelgruppe" VARCHAR(250),
  "Kategorie" VARCHAR(250)
);

CREATE TABLE "Vertrag_Waren" (
  "VID" INT NOT NULL,
  "WID" INT NOT NULL,
  "Menge" INT NOT NULL,
  PRIMARY KEY("VID","WID")
);

ALTER TABLE "Kunden" ADD FOREIGN KEY ("Lieferadresse_ID") REFERENCES "Adressen" ("AdresseID");

ALTER TABLE "Kunden" ADD FOREIGN KEY ("Rechnungsadresse_ID") REFERENCES "Adressen" ("AdresseID");

ALTER TABLE "Vertraege" ADD FOREIGN KEY ("KID") REFERENCES "Kunden" ("KID");

ALTER TABLE "Vertrag_Waren" ADD FOREIGN KEY ("VID") REFERENCES "Vertraege" ("VID");

ALTER TABLE "Vertrag_Waren" ADD FOREIGN KEY ("WID") REFERENCES "Waren" ("WID");
