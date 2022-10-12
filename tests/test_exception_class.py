import traceback
import logging
logging.basicConfig(filename='../src/test_balance_weights.log')
import test_Exception as Test

a = 1000
def _add(a):
    if a >800:
        raise Test.my_ERROR(a)
    a +=200
    return a

try:
    _add(a)
except Test.my_ERROR as e:
    logging.error(traceback.format_exc())
    print(e)