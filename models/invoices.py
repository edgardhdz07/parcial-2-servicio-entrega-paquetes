from models import clients, packages
from controllers import invoicesController
from datetime import date

Invoices = [
    {
        "id": 1,
        "date": date(2021, 4, 10),
        "client": clients.Clients[0],
        "items": [packages.Packages[0]],
        "total": 7550.0
    },
    {
        "id": 2,
        "date": date(2021, 3, 27),
        "client": clients.Clients[1],
        "items": [packages.Packages[1]],
        "total": 5050.0
    }
]
