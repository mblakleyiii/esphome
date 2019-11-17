#pragma once

#include "esphome/core/component.h"
#include "esphome/core/log.h"

#include "NonBlockingRtttl.h"

namespace esphome {
namespace rtttlplayer {

static const char *TAG = "rtttl";

class RtttlComponent : public Component {

 public:
  void set_song(std::string song) { this->song_ = song; }
  void set_pin(int pin) { this->pin_ = pin; }
  void play() {
      if (this->song_.length() > 0) {
        ESP_LOGD(TAG, "Start Playing");
        ESP_LOGV(TAG, "  Song: %s", this->song_.c_str());
        delay(10);
        rtttl::begin(this->pin_, this->song_.c_str());
      }
  };
  void stop() { ESP_LOGD(TAG, "Stop Playing"); rtttl::stop(); };

  void setup() override { pinMode(this->pin_, OUTPUT); }
  void loop() override { if (!rtttl::done()) rtttl::play(); };
  void dump_config() override { ESP_LOGCONFIG(TAG, "RTTTL:"); };

 protected:
  std::string song_;
  int pin_;

};

template<typename... Ts> class PlayAction : public Action<Ts...>, public Parented<RtttlComponent> {
 public:
  void play(Ts... x) override {
      this->parent_->play();
  }
};

template<typename... Ts> class StopAction : public Action<Ts...>, public Parented<RtttlComponent> {
 public:
  void play(Ts... x) override { this->parent_->stop(); }
};

template<typename... Ts> class SetSongAction : public Action<Ts...>, public Parented<RtttlComponent> {
 public:
  TEMPLATABLE_VALUE(std::string, song)
  void play(Ts... x) override {
    auto song = this->song_.value(x...);
    this->parent_->set_song(song);
  }
};

}
}