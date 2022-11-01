import sys
from CONST_ENV import ENV_PATH as PATH
from utils.update_info import update_metadata
import utils.file_operations as fop

CONFIG = fop.load_lsyers_config(PATH.CONFIG_PATH)
update_metadata(PATH.JSON_PATH, CONFIG)