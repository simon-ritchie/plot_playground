import os

if __name__ == '__main__':
    os.system('python setup.py install')
    os.system('nosetests -s')
