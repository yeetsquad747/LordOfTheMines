shopItems = {
    "lucky totem": {
        "name": "lucky totem",
        "price": 10000,
        "description": "A lucky totem that will give you better luck. Allows you to possibly mine double ore.",
        "craftable": True,
        "sellable": False,
        "item_type": "totem",
        "totem_chance": 5,
        "totem_multiply": 2,
        "recipe": {
            "diamond": 8,
            "platinum": 1,
        },
        "contents": {
            "lucky totem": 1
        },
    },
    "mega totem": {
        "name": "mega totem",
        "price": 50000,
        "description": "A mega totem that will give you better luck. Allows you to possibly mine triple ore.",
        "craftable": True,
        "sellable": False,
        "item_type": "totem",
        "totem_chance": 5,
        "totem_multiply": 3,
        "recipe": {
            "diamond": 40,
            "platinum": 5,
        },
        "contents": {
            "mega totem": 1
        },
    },
    "collectors coin": {
        "name": "collectors coin",
        "price": 1000000,
        "description": "A coin that is for only the richest. No real use but nice.",
        "craftable": False,
        "sellable": True,
        "item_type": "collectors_item",
        "contents": {
            "collectors coin": 1
        }
    },
    "starter crate": {
        "name": "starter crate",
        "price": 5000,
        "description": "A crate that contains a starter pack of ores.",
        "craftable": False,
        "sellable": True,
        "item_type": "crate",
        "contents": {
            "stone": 100,
            "coal": 100,
            "copper": 100,
            "amethyst": 100,
            "iron": 100,
        }
    },
    "metal crate": {
        "name": "metal crate",
        "price": 30000,
        "description": "A crate that contains a pack of all the metals",
        "craftable": False,
        "sellable": True,
        "item_type": "crate",
        "contents": {
            "copper": 100,
            "iron": 100,
            "silver": 100,
            "gold": 100,
        }
    },
    "gem crate": {
        "name": "gem crate",
        "price": 80000,
        "description": "A crate that contains a pack of all the gems",
        "craftable": False,
        "sellable": True,
        "item_type": "crate",
        "contents": {
            "amethyst": 100,
            "emerald": 100,
            "diamond": 100,
        }
    },
}