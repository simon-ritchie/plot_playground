import os
import time
import multiprocessing as mp
import subprocess as sp

JUPYTER_TEST_PORT = 18080


def run_jupyter_process():
    """
    Start Jupyter for testing.
    """
    os.system(
        'jupyter notebook --no-browser --port={jupyter_test_port} &'.format(
            jupyter_test_port=JUPYTER_TEST_PORT
        ))
    print(200, 100)


def is_jupyter_started():
    """
    Get the boolean value as to whether Jupyter for testing has
    been started or not.

    Returns
    -------
    result : bool
        If it is started this function will returns True.
    """
    out = sp.check_output(
        ['jupyter', 'notebook', 'list'])
    out = str(out)
    is_in = str(JUPYTER_TEST_PORT) in out
    if is_in:
        return True
    return False


if __name__ == '__main__':
    jupyter_process = mp.Process(target=run_jupyter_process)
    jupyter_process.start()

    os.system('python setup.py install')
    while not is_jupyter_started():
        print('continue')
        time.sleep(1)
    os.system('nosetests -s')
    jupyter_process.terminate()
