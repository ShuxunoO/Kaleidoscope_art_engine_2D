from tqdm import tqdm, trange
import time

def fun1(num):
    return range(num)


if __name__ == "main":
    for i in tqdm(range(20), desc='NFT generating progress',unit= "个", postfix={'value': 520}):
        tqdm.write('当前i={}'.format(i))
        time.sleep(0.2)