Alle POST brauchen keine id

## Kunden

/customers GET
[
    {
        "kid": int,
        "firma": "string",
        ...
        "lieferadresse": {
            "straße" : "String",
            "hausnummer" : int, 
            ...
        },
        ...
    },
    ...
]

/customers/<id> GET, POST und PUT
{
    "firma": "string",
    ...
    "lieferadresse": {
        "straße" : "String",
        "hausnummer" : int, 
        ...
    },
    ...
}

/customers/<id> DELETE

## Waren 

/wares GET
[
    {
        "wid": int
        ...
    },
    ...
]

/wares/<id> GET, POST und PUT
{
    "bezeichnung" : "String",
    ...
}

## Verträge

/contracts GET
[
    {
        "vid": int,
        "kunde": {
            siehe /customers/<id> GET
        },
        "ware": {
            siehe /wares/<id> GET
            }
        "menge": int,
        "datum": "String",
        "mwst": float,
        "annahme": boolean,
        "user":{
            siehe /users/<id> GET
        }
    },
    ...
]

/contracts/<id> GET, POST und PUT
{
    "vid": int,
    "kunde": {
        siehe /customers/<id> GET
    },
    "ware": {
        siehe /wares/<id> GET
        }
    "menge": int,
    "datum": "String",
    "mwst": float,
    "annahme": boolean,
    "user":{
        siehe /users/<id> GET
    }
}

/contracts/<id> DELETE

## Benutzer

/users GET
[
    {
        "id": int,
        "username": "String",
        "role": "String"
    },
    ...
]

/users/<id> GET
{
    "username": "String",
    "role": "String"
}

/users/<id> POST und PUT
{
    "username": "String",
    "role":"String",
    "password": "String"            in SHA512
}

/users/<id>/password GET
{
    "password": "String"            in SHA512
}

/users/<id>/password PUT 
{
    "password": "String"            in SHA512
}

/users/<id> DELETE




















