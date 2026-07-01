import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_UART_ID
from esphome.components import uart, sensor
from esphome import pins

AUTO_LOAD = ["uart"]

mppt_reader_ns = cg.esphome_ns.namespace("mppt_reader")
MpptReaderComponent = mppt_reader_ns.class_("MpptReader", cg.Component, uart.UARTDevice)

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
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    uart_component = await cg.get_variable(config[CONF_UART_ID])
    cg.add(var.set_uart(uart_component))

    de_pin = await cg.gpio_pin_expression(config["de_pin"])
    cg.add(var.set_de_pin(de_pin))

    for key in SENSORS:
        sens = await sensor.new_sensor(config[key])
        cg.add(getattr(var, f"set_{key}_sensor")(sens))
