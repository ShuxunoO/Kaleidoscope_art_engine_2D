import sys
from CONST_ENV import ENV_PATH as PATH
import utils.update_info as update
import utils.file_operations as fop

CONFIG = fop.load_json(PATH.CONFIG_PATH)
update.update_metadata(CONFIG)
# update.shuffle(1, 10)