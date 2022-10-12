class my_ERROR(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "current value " + str(self.value) + "is larger than _SUM"

# a = 1000
# def _add(a):
#     if a >800:
#         raise my_ERROR(a)
#     a +=200
#     return a

# try:
#     _add(a)
# except my_ERROR as e:
#     logging.error(traceback.format_exc())
#     print(e)