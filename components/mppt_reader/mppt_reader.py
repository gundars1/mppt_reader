import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_UART_ID
from esphome.components import uart, sensor
from esphome import pins
from . import mppt_reader_ns, MpptReaderComponent

AUTO_LOAD = ["uart"]

SENSORS = ["pv_voltage", "batt_voltage", "current", "daily_wh", "total_wh"]

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MpptReaderComponent),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    cv.Required("de_pin"): pins.gpio_output_pin_schema,
    **{
        cv.Required(key): sensor.sensor_schema()
        for key in SENSORS
    }
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    # 1. Paņemam UART un DE pin mainīgos no konfigurācijas
    uart_component = await cg.get_variable(config[CONF_UART_ID])
    de_pin = await cg.gpio_pin_expression(config["de_pin"])

    # 2. Nododam tos tieši C++ konstruktoram (atbilst: MpptReader(uart, de_pin))
    var = cg.new_Pvariable(config[CONF_ID], uart_component, de_pin)
    await cg.register_component(var, config)

    # 3. Piereģistrējam visus sensorus
    for key in SENSORS:
        sens = await sensor.new_sensor(config[key])
        cg.add(getattr(var, f"set_{key}_sensor")(sens))
