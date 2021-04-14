from models import tracks

Packages = [
    {
        "id": 1,
        "name": "paquete_1",
        "price": 50.000,
        "track": {
            "id": 1,
            "origin":  tracks.Tracks[2]["origin"],
            "destination": tracks.Tracks[2]["destination"],
            "cost": tracks.Tracks[2]["cost"]
        }

    },
    {
        "id": 2,
        "name": "paquete_2",
        "price": 50.000,
        "track": {
            "id": 2,
            "origin": tracks.Tracks[1]["origin"],
            "destination": tracks.Tracks[1]["destination"],
            "cost": tracks.Tracks[1]["cost"]
        }

    }
]


