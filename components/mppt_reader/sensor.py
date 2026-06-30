import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_UART_ID,
    CONF_UPDATE_INTERVAL,
)
from esphome import pins
from esphome.components import uart, sensor

AUTO_LOAD = ["uart"]

mppt_reader_ns = cg.esphome_ns.namespace("mppt_reader")
MPPTReader = mppt_reader_ns.class_("MPPTReader", cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MPPTReader),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    cv.Required("de_pin"): pins.gpio_output_pin_schema,
    cv.Optional(CONF_UPDATE_INTERVAL, default="10s"): cv.update_interval,
    cv.Required("pv_voltage"): sensor.sensor_schema(),
    cv.Required("batt_voltage"): sensor.sensor_schema(),
    cv.Required("current"): sensor.sensor_schema(),
    cv.Required("daily_wh"): sensor.sensor_schema(),
    cv.Required("total_wh"): sensor.sensor_schema(),
})

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    cg.register_component(var, config)
    uart_component = yield cg.get_variable(config[CONF_UART_ID])
    cg.add(var.set_uart(uart_component))

    de_pin = yield cg.gpio_pin_expression(config["de_pin"])
    cg.add(var.set_de_pin(de_pin))

    for key in ["pv_voltage", "batt_voltage", "current", "daily_wh", "total_wh"]:
        sens = yield sensor.new_sensor(config[key])
        cg.add(getattr(var, f"set_{key}_sensor")(sens))

    if CONF_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))
