#include "mppt_reader.h"
#include "esphome/core/log.h"
#include "esphome/core/hal.h"

namespace esphome {
namespace mppt_reader {

static const char *const TAG = "mppt_reader";

// Piemērs: 8-baitu pieprasījums, ko tu lietoji Arduino kodā.
// Pielāgo, ja tavs īstais kadrs atšķiras.
static const uint8_t REQUEST_FRAME[8] = {
    0xAA, 0x55, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00  // pēdējo baitu aizpildām ar checksum
};

static const uint8_t RESPONSE_LEN = 93;

MpptReader::MpptReader(uart::UARTComponent *parent, GPIOPin *de_pin)
    : uart::UARTDevice(parent), de_pin_(de_pin) {}

void MpptReader::setup() {
  this->de_pin_->setup();
  this->de_pin_->digital_write(false);  // sākumā RX režīms
  this->last_query_ = millis();
}

void MpptReader::loop() {
  uint32_t now = millis();
  if (now - this->last_query_ < this->update_interval_ms_)
    return;

  this->last_query_ = now;

  this->send_request_();
  if (!this->read_response_()) {
    ESP_LOGW(TAG, "MPPT atbilde nav derīga");
  }
}

void MpptReader::send_request_() {
  uint8_t frame[8];
  memcpy(frame, REQUEST_FRAME, 8);

  // checksum = sum pirmie 7 baiti
  frame[7] = calc_checksum_(frame, 7);

  // DE/RE HIGH → TX
  this->de_pin_->digital_write(true);
  delay(2);

  this->write_array(frame, 8);
  this->flush();

  delay(2);
  // DE/RE LOW → RX
  this->de_pin_->digital_write(false);
}

bool MpptReader::read_response_() {
  uint8_t buf[RESPONSE_LEN];
  uint32_t start = millis();

  // gaidām līdz atnāk viss kadrs vai timeout
  uint8_t pos = 0;
  while (pos < RESPONSE_LEN && millis() - start < 200) {
    if (this->available()) {
      buf[pos++] = this->read();
    } else {
      delay(1);
    }
  }

  if (pos < RESPONSE_LEN) {
    ESP_LOGW(TAG, "Saņemti tikai %u baiti, gaidīju %u", pos, RESPONSE_LEN);
    return false;
  }

  // checksum pārbaude: sum pirmie 92 baiti, salīdzinām ar pēdējo
  uint8_t cs = calc_checksum_(buf, RESPONSE_LEN - 1);
  if (cs != buf[RESPONSE_LEN - 1]) {
    ESP_LOGW(TAG, "Checksum kļūda: gaidīju 0x%02X, saņēmu 0x%02X", cs, buf[RESPONSE_LEN - 1]);
    return false;
  }

  // Šeit izmanto tās pašas adreses/offsetus, ko Arduino kodā:
  // Piemērs (pielāgo pēc savas tabulas!):

  // Pieņemsim:
  // PV V: 2 baiti, /10, offset 10
  // Batt V: 2 baiti, /10, offset 12
  // Current: 2 baiti, /100, offset 14
  // Daily Wh: 4 baiti, raw, offset 20
  // Total Wh: 4 baiti, raw, offset 24

  auto get_u16 = [&](int idx) -> uint16_t {
    return (uint16_t(buf[idx]) << 8) | uint16_t(buf[idx + 1]);
  };

  auto get_u32 = [&](int idx) -> uint32_t {
    return (uint32_t(buf[idx]) << 24) | (uint32_t(buf[idx + 1]) << 16) |
           (uint32_t(buf[idx + 2]) << 8) | uint32_t(buf[idx + 3]);
  };

  float pv_v = get_u16(10) / 10.0f;
  float batt_v = get_u16(12) / 10.0f;
  float curr_a = get_u16(14) / 100.0f;
  float daily_wh = (float) get_u32(20);
  float total_wh = (float) get_u32(24);

  if (this->pv_voltage_ != nullptr)
    this->pv_voltage_->publish_state(pv_v);
  if (this->batt_voltage_ != nullptr)
    this->batt_voltage_->publish_state(batt_v);
  if (this->current_ != nullptr)
    this->current_->publish_state(curr_a);
  if (this->daily_wh_ != nullptr)
    this->daily_wh_->publish_state(daily_wh);
  if (this->total_wh_ != nullptr)
    this->total_wh_->publish_state(total_wh);

  ESP_LOGD(TAG, "PV=%.1f V, Batt=%.1f V, I=%.2f A, Daily=%.0f Wh, Total=%.0f Wh",
           pv_v, batt_v, curr_a, daily_wh, total_wh);

  return true;
}

uint8_t MpptReader::calc_checksum_(const uint8_t *data, uint8_t len) {
  uint16_t sum = 0;
  for (uint8_t i = 0; i < len; i++)
    sum += data[i];
  return (uint8_t) (sum & 0xFF);
}

}  // namespace mppt_reader
}  // namespace esphome
