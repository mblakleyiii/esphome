import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.automation import maybe_simple_id
from esphome.components import output
from esphome.const import CONF_ID, CONF_OUTPUT

rtttl_ns = cg.esphome_ns.namespace('rtttlplayer')
RtttlComponent = rtttl_ns.class_('RtttlComponent', cg.Component)
PlayAction = rtttl_ns.class_('PlayAction', automation.Action)
StopAction = rtttl_ns.class_('StopAction', automation.Action)
SetSongAction = rtttl_ns.class_('SetSongAction', automation.Action)

CONF_PIN = 'pin'
CONF_SONG = 'song'

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.declare_id(RtttlComponent),
    cv.Required(CONF_PIN): cv.int_,
    cv.Optional(CONF_SONG, default=""): cv.string_strict,
}).extend(cv.COMPONENT_SCHEMA)

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)

    cg.add(var.set_pin(config[CONF_PIN]))
    cg.add(var.set_song(config[CONF_SONG]))

    cg.add_library('NonBlockingRTTTL', None)

@automation.register_action('rtttl.play', PlayAction, maybe_simple_id({
    cv.Required(CONF_ID): cv.use_id(RtttlComponent),
}))
def rtttl_play_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    yield cg.register_parented(var, config[CONF_ID])
    yield var

@automation.register_action('rtttl.stop', StopAction, maybe_simple_id({
    cv.Required(CONF_ID): cv.use_id(RtttlComponent),
}))
def rtttl_stop_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    yield cg.register_parented(var, config[CONF_ID])
    yield var

@automation.register_action('rtttl.set_song', SetSongAction, cv.Schema({
    cv.Required(CONF_ID): cv.use_id(RtttlComponent),
    cv.Required(CONF_SONG): cv.templatable(cv.string_strict),
}))
def rtttl_set_song_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    yield cg.register_parented(var, config[CONF_ID])
    template_ = yield cg.templatable(config[CONF_SONG], args, cg.std_string)
    cg.add(var.set_song(template_))
    yield var