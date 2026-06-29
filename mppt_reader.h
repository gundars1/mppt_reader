#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/gpio/output/gpio_output.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace mppt_reader {

class MPPTReader : public Component {
 public:
  uart::UARTComponent *uart_{nullptr};
  gpio::GPIOOutput *dir_pin_{nullptr};

  sensor::Sensor *batt_v_{nullptr};
  sensor::Sensor *pv_v_{nullptr};
  sensor::Sensor *charge_a_{nullptr};
  sensor::Sensor *daily_{nullptr};
  sensor::Sensor *total_{nullptr};
  sensor::Sensor *power_{nullptr};

  void set_uart(uart::UARTComponent *u) { uart_ = u; }
  void set_dir_pin(gpio::GPIOBinaryOutput *d) { dir_pin_ = d; }

  void set_batt_voltage_sensor(sensor::Sensor *s) { batt_v_ = s; }
  void set_pv_voltage_sensor(sensor::Sensor *s) { pv_v_ = s; }
  void set_charge_current_sensor(sensor::Sensor *s) { charge_a_ = s; }
  void set_daily_energy_sensor(sensor::Sensor *s) { daily_ = s; }
  void set_total_energy_sensor(sensor::Sensor *s) { total_ = s; }
  void set_battery_power_sensor(sensor::Sensor *s) { power_ = s; }

  void setup() override;
  void loop() override;
};

}  // namespace mppt_reader
}  // namespace esphome
