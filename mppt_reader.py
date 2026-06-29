import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor, output
from esphome.const import CONF_ID

mppt_reader_ns = cg.esphome_ns.namespace("mppt_reader")
MPPTReader = mppt_reader_ns.class_("MPPTReader", cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MPPTReader),

    cv.Required("uart_id"): cv.use_id(uart.UARTComponent),
    cv.Required("dir_pin"): cv.use_id(output.BinaryOutput),

    cv.Required("batt_voltage"): cv.use_id(sensor.Sensor),
    cv.Required("pv_voltage"): cv.use_id(sensor.Sensor),
    cv.Required("charge_current"): cv.use_id(sensor.Sensor),
    cv.Required("daily_energy"): cv.use_id(sensor.Sensor),
    cv.Required("total_energy"): cv.use_id(sensor.Sensor),
    cv.Required("battery_power"): cv.use_id(sensor.Sensor),
})



async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    uart_comp = await cg.get_variable(config["uart_id"])
    cg.add(var.set_uart(uart_comp))

    dir_pin = await cg.get_variable(config["dir_pin"])
    cg.add(var.set_dir_pin(dir_pin))

    cg.add(var.set_batt_voltage_sensor(await cg.get_variable(config["batt_voltage"])))
    cg.add(var.set_pv_voltage_sensor(await cg.get_variable(config["pv_voltage"])))
    cg.add(var.set_charge_current_sensor(await cg.get_variable(config["charge_current"])))
    cg.add(var.set_daily_energy_sensor(await cg.get_variable(config["daily_energy"])))
    cg.add(var.set_total_energy_sensor(await cg.get_variable(config["total_energy"])))
    cg.add(var.set_battery_power_sensor(await cg.get_variable(config["battery_power"])))

