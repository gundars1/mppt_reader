async def to_code(config):
    # 1. Vispirms paņemam mainīgos no konfigurācijas
    uart_component = await cg.get_variable(config[CONF_UART_ID])
    de_pin = await cg.gpio_pin_expression(config["de_pin"])

    # 2. Nododam tos tieši C++ konstruktoram, kad veidojam jauno objektu (MpptReader(uart, de_pin))
    var = cg.new_Pvariable(config[CONF_ID], uart_component, de_pin)
    await cg.register_component(var, config)

    # 3. Piereģistrējam sensorus (tas paliek nemainīgs)
    for key in SENSORS:
        sens = await sensor.new_sensor(config[key])
        cg.add(getattr(var, f"set_{key}_sensor")(sens))
