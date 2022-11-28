import sys
from CONST_ENV import ENV_PATH as PATH
import utils.update_info as update
import utils.file_operations as fop

CONFIG = fop.load_json(PATH.CONFIG_PATH)
# 混合元素之前要先删掉文件夹中的所有文件，防止前后两次混合的元素弄混
# update.update_metadata(CONFIG)
update.shuffle(1, 5)