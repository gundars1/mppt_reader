from esphome import codegen as cg, config_validation as cv
from esphome.components import uart
from esphome.const import (
    CONF_ID,
    CONF_UPDATE_INTERVAL,
)

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]

mppt_ns = cg.esphome_ns.namespace("mppt_reader")
MpptReader = mppt_ns.class_("MpptReader", cg.Component, uart.UARTDevice)

CONF_DE_PIN = "de_pin"
CONF_PV_VOLTAGE = "pv_voltage"
CONF_BATT_VOLTAGE = "batt_voltage"
CONF_CURRENT = "current"
CONF_DAILY_WH = "daily_wh"
CONF_TOTAL_WH = "total_wh"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MpptReader),
    cv.Required(CONF_DE_PIN): cv.pin,
    cv.Optional(CONF_UPDATE_INTERVAL, default="10s"): cv.update_interval,
    cv.Required(CONF_PV_VOLTAGE): cv.sensor.schema(
        unit_of_measurement="V",
        accuracy_decimals=1,
    ),
    cv.Required(CONF_BATT_VOLTAGE): cv.sensor.schema(
        unit_of_measurement="V",
        accuracy_decimals=1,
    ),
    cv.Required(CONF_CURRENT): cv.sensor.schema(
        unit_of_measurement="A",
        accuracy_decimals=2,
    ),
    cv.Required(CONF_DAILY_WH): cv.sensor.schema(
        unit_of_measurement="Wh",
        accuracy_decimals=0,
    ),
    cv.Required(CONF_TOTAL_WH): cv.sensor.schema(
        unit_of_measurement="Wh",
        accuracy_decimals=0,
    ),
}).extend(uart.UART_DEVICE_SCHEMA)


async def to_code(config):
    uart_var = await uart.new_uart_device(config)

    de_pin = await cg.gpio_pin_expression(config[CONF_DE_PIN])

    var = cg.new_Pvariable(config[CONF_ID], uart_var, de_pin)
    await cg.register_component(var, config)

    pv = await cg.sensor.new_sensor(config[CONF_PV_VOLTAGE])
    batt = await cg.sensor.new_sensor(config[CONF_BATT_VOLTAGE])
    curr = await cg.sensor.new_sensor(config[CONF_CURRENT])
    daily = await cg.sensor.new_sensor(config[CONF_DAILY_WH])
    total = await cg.sensor.new_sensor(config[CONF_TOTAL_WH])

    cg.add(var.set_pv_voltage_sensor(pv))
    cg.add(var.set_batt_voltage_sensor(batt))
    cg.add(var.set_current_sensor(curr))
    cg.add(var.set_daily_wh_sensor(daily))
    cg.add(var.set_total_wh_sensor(total))
