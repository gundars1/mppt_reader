#pragma once

#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/core/component.h"
#include "esphome/core/gpio.h"

namespace esphome {
namespace mppt_reader {

class MpptReader : public Component, public uart::UARTDevice {
 public:
  MpptReader(uart::UARTComponent *parent, GPIOPin *de_pin);

  void setup() override;
  void loop() override;

  void set_pv_voltage_sensor(sensor::Sensor *s) { pv_voltage_ = s; }
  void set_batt_voltage_sensor(sensor::Sensor *s) { batt_voltage_ = s; }
  void set_current_sensor(sensor::Sensor *s) { current_ = s; }
  void set_daily_wh_sensor(sensor::Sensor *s) { daily_wh_ = s; }
  void set_total_wh_sensor(sensor::Sensor *s) { total_wh_ = s; }

 protected:
  void send_request_();
  bool read_response_();
  uint8_t calc_checksum_(const uint8_t *data, uint8_t len);

  GPIOPin *de_pin_;
  sensor::Sensor *pv_voltage_{nullptr};
  sensor::Sensor *batt_voltage_{nullptr};
  sensor::Sensor *current_{nullptr};
  sensor::Sensor *daily_wh_{nullptr};
  sensor::Sensor *total_wh_{nullptr};

  uint32_t last_query_{0};
  uint32_t update_interval_ms_{10000};
};

}  // namespace mppt_reader
}  // namespace esphome
