import multiprocessing

def cal(x):
    with open('data.txt', 'w') as f:
        f.write(str(x))


