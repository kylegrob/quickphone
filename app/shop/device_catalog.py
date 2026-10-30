"""Starter list of devices the shop repairs: (device type, brand, model).

Check-in picks a device from this list (DEVICE_MODEL table); staff add anything missing from
the check-in screen. The data migration and the training seed both load it, so a new
database starts with a usable list. Edit freely: it is a convenience, not a requirement."""

STARTER_DEVICES = [
    ("Phone", "Apple", "iPhone 11"), ("Phone", "Apple", "iPhone 12"), ("Phone", "Apple", "iPhone 13"),
    ("Phone", "Apple", "iPhone 14"), ("Phone", "Apple", "iPhone 15"), ("Phone", "Apple", "iPhone SE (2nd gen)"),
    ("Phone", "Samsung", "Galaxy S21"), ("Phone", "Samsung", "Galaxy S22"), ("Phone", "Samsung", "Galaxy S23"),
    ("Phone", "Samsung", "Galaxy A14"), ("Phone", "Samsung", "Galaxy A54"),
    ("Phone", "Google", "Pixel 6"), ("Phone", "Google", "Pixel 7"), ("Phone", "Google", "Pixel 8"),
    ("Tablet", "Apple", "iPad 9th gen"), ("Tablet", "Apple", "iPad 10th gen"), ("Tablet", "Apple", "iPad Air"),
    ("Tablet", "Samsung", "Galaxy Tab A8"),
    ("Laptop", "Apple", "MacBook Air"), ("Laptop", "Lenovo", "IdeaPad 3"), ("Laptop", "Lenovo", "ThinkPad E14"),
    ("Game console", "Nintendo", "Switch"), ("Game console", "Nintendo", "Switch Lite"),
    ("Game console", "Sony", "PlayStation 5"), ("Game console", "Microsoft", "Xbox Series X"),
]
