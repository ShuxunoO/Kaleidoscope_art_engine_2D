import time
from progressbar import *

total = 1000


def test_func():
    time.sleep(0.01)


progress = ProgressBar()
for i in progress(range(1000)):
    test_func()
