import esphome.codegen as cg
import esphome.config_validation as cv

# Definējam C++ namespace un komponentes identifikāciju
mppt_reader_ns = cg.esphome_ns.namespace("mppt_reader")
MpptReaderComponent = mppt_reader_ns.class_("MpptReader", cg.Component)

# Tukša shēma, jo reālo YAML konfigurāciju apstrādās mppt_reader.py failā
CONFIG_SCHEMA = cv.Schema({})
