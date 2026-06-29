#include "mppt_reader.h"

namespace esphome {
namespace mppt_reader {

void MPPTReader::setup() {
  // Nothing needed here
}

void MPPTReader::loop() {
  static uint32_t last = 0;

  if (millis() - last > 10000) {
    last = millis();

    uint8_t cmd[] = {0x01, 0xB1, 0x01, 0x00, 0x00, 0x00, 0x00, 0xB3};

    if (dir_pin_) dir_pin_->turn_on();   // TX mode
    if (uart_) {
      uart_->write_array(cmd, 8);
      uart_->flush();
    }
    if (dir_pin_) dir_pin_->turn_off();  // RX mode
  }

  if (uart_ && uart_->available() >= 93) {
    uint8_t buf[93];
    for (int i = 0; i < 93; i++) buf[i] = uart_->read();

    uint32_t sum = 0;
    for (int i = 0; i < 92; i++) sum += buf[i];
    if ((sum & 0xFF) != buf[92]) return;

    float battV = ((buf[32] << 8) | buf[33]) / 100.0;
    float pvV = ((buf[30] << 8) | buf[31]) / 10.0;
    float chargeA = ((buf[34] << 8) | buf[35]) / 100.0;

    uint32_t dailyE =
        (buf[44] << 24) | (buf[45] << 16) | (buf[46] << 8) | buf[47];

    uint32_t totalE =
        (buf[48] << 24) | (buf[49] << 16) | (buf[50] << 8) | buf[51];

    float battPower = battV * chargeA;

    if (batt_v_) batt_v_->publish_state(battV);
    if (pv_v_) pv_v_->publish_state(pvV);
    if (charge_a_) charge_a_->publish_state(chargeA);
    if (daily_) daily_->publish_state(dailyE);
    if (total_) total_->publish_state(totalE);
    if (power_) power_->publish_state(battPower);
  }
}

}  // namespace mppt_reader
}  // namespace esphome
