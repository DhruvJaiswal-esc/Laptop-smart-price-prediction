from database.database import SessionLocal
from database.crud import save_prediction, get_prediction_history

db = SessionLocal()


class Dummy:

    brand = "ASUS"
    processor = "Intel Core i5-13420H"
    graphic_processor = "RTX 4050"

    capacity = 16
    ram_type = "DDR5"
    ram_speed = 4800

    ssd_capacity = 512
    ssd_type = "NVMe"

    graphics_memory = 6

    battery_capacity = 57
    battery_type = "Li-Ion"

    weight = 2.1

    warranty = 1

    wi_fi_version = "Wi-Fi 6"

    bluetooth_version = "5.3"


prediction = save_prediction(

    db,

    Dummy(),

    predicted_price=85999,

    predicted_category="Gaming"

)

print(prediction.id)

history = get_prediction_history(db)

print(history)

db.close()