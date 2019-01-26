"""
A module describing Jupyter's general purpose control
function for testing.

Notes
-----
It is necessary to use it with Jupyter running.

See Also
--------
run_tests.py
    Handle startup and shutdown of Jupyter.
"""

import subprocess as sp
import time
import json
import os

from selenium.webdriver.common.keys import Keys

from plot_playground.common import settings
from plot_playground.common import selenium_helper

JUPYTER_ROOT_URL = 'http://localhost:{jupyter_test_port}/'.format(
    jupyter_test_port=settings.JUPYTER_TEST_PORT
)

RUN_ALL_CELLS_SELECTOR_ID_STR = 'run_all_cells'
OUTPUT_TEXT_SELECTOR_CLASS_STR = 'output_subarea'
CELL_MENU_SELECTOR_ID_STR = 'cell_menu'
INPUT_SELECTOR_CLASS_STR = 'input'
HEADER_CONTAINER_SELECTOR_ID_STR = 'header-container'
MENU_BAR_CONTAINER_SELECTOR_ID_STR = 'menubar-container'


def empty_test_ipynb_code_cell():
    """
    Empty the code cell of the test ipynb file.
    """
    if not os.path.exists(TEST_JUPYTER_NOTE_PATH):
        return

    ipynb_dict = _read_test_ipynb_dict()
    code_cell_idx = _get_ipynb_code_cell_idx(
        ipynb_dict=ipynb_dict)
    update_ipynb_test_source_code(source_code='')


def get_jupyter_root_url_with_token():
    """
    Get root URL of Jupyter's local server including
    token.

    Returns
    -------
    root_url : str
        The root URL of the target Jupyter.

    Raises
    ------
    Exception
        If Jupyter is not running.
    """
    token_str = get_jupyter_token()
    root_url = JUPYTER_ROOT_URL + token_str
    return root_url


def get_jupyter_token():
    """
    Get the token string of Jupyter for testing.

    Returns
    -------
    token_str : str
        A string of token including the parameter part of
        "?token=".

    Raises
    ------
    Exception
        If Jupyter is not running.
    """
    out = sp.check_output(
        ['jupyter', 'notebook', 'list'])
    out = str(out)
    is_in = JUPYTER_ROOT_URL in out
    if not is_in:
        raise Exception("Jupyter's local server is not running. Please check whether it is started normally in the run_tests.py module.")
    token_str = out.split(JUPYTER_ROOT_URL)[1]
    token_str = token_str.split(' :: ')[0]
    return token_str


TEST_JUPYTER_NOTE_NAME = 'test_on_jupyter'
TEST_JUPYTER_NOTE_URL = "http://localhost:{jupyter_test_port}/notebooks/{test_jupyter_note_name}.ipynb".format(
    jupyter_test_port=settings.JUPYTER_TEST_PORT,
    test_jupyter_note_name=TEST_JUPYTER_NOTE_NAME
)
TEST_JUPYTER_NOTE_PATH = os.path.join(
    settings.ROOT_DIR,
    TEST_JUPYTER_NOTE_NAME + '.ipynb',
)


def open_test_jupyter_note_book():
    """
    Open the Jupyter notebook for testing.

    Raises
    ------
    Exception
        If Jupyter is not running.

    Notes
    -----
    If the note does not exist in the target path for some
    reason, add a test notebook to the following path
    beforehand and place only one code cell.

    plot_playground/tests/notes/test_on_jupyter.ipynb
    """
    driver = selenium_helper.start_webdriver()
    root_url = get_jupyter_root_url_with_token()
    driver.get(root_url)
    test_note_url = TEST_JUPYTER_NOTE_URL
    driver.get(test_note_url)
    loop_count = 0
    while loop_count < 10:
        if driver.title == TEST_JUPYTER_NOTE_NAME:
            break
        loop_count += 1
        time.sleep(1)
    time.sleep(3)


def run_test_code(sleep_seconds=1):
    """
    Execute the code of the test cell.

    Parameters
    ----------
    sleep_seconds : int, default 1
        The number of seconds to sleep after starting execution
        of code cells.

    Raises
    ------
    Exception
        - If the menu element for cell execution can not be found.
        - If more than one menu element for cell execution is found.
    """
    _assert_current_page_is_test_notebook()
    display_cell_menu()
    driver = selenium_helper.driver
    run_all_menu_elem_list = driver.find_elements_by_id(
        RUN_ALL_CELLS_SELECTOR_ID_STR
    )
    if not run_all_menu_elem_list:
        raise Exception('No menu element for cell execution was found.')
    if len(run_all_menu_elem_list) != 1:
        raise Exception('More than one menu element for cell execution was found.')
    run_all_menu_elem = run_all_menu_elem_list[0]
    run_all_menu_elem.click()
    time.sleep(sleep_seconds)


def display_cell_menu():
    """
    Display the menu of the cell.

    Raises
    ------
    Exception
        - If the menu of the cell does not exist.
        - If there are multiple menu of cells.
    """
    _assert_current_page_is_test_notebook()
    driver = selenium_helper.driver
    cell_menu_elem_list = driver.find_elements_by_id(
        CELL_MENU_SELECTOR_ID_STR
    )
    if not cell_menu_elem_list:
        raise Exception('The menu element of the cell does not exist.')
    if len(cell_menu_elem_list) != 1:
        raise Exception('There are two or more cell menu elements.')
    script = '$("#{cell_menu_selector_id_str}").css("display", "block");'.format(
        cell_menu_selector_id_str=CELL_MENU_SELECTOR_ID_STR
    )
    driver.execute_script(script)


def get_test_code_text_output():
    """
    Get the text of the output.

    Returns
    -------
    output_text : str
        Text on the output cell.
    """
    _assert_current_page_is_test_notebook()
    _assert_only_one_output_cell_exists()
    driver = selenium_helper.driver
    output_cell_elem = driver.find_element_by_class_name(
        OUTPUT_TEXT_SELECTOR_CLASS_STR
    )
    output_text = output_cell_elem.text
    return output_text


def output_text_cell_exists():
    """
    Get boolean as to whether output cell exists.

    Returns
    -------
    result : bool
        If the cell exists, it is set to true.
    """
    driver = selenium_helper.driver
    output_cell_elem_list = driver.find_elements_by_class_name(
        OUTPUT_TEXT_SELECTOR_CLASS_STR)
    if not output_cell_elem_list:
        return False
    return True


def _assert_only_one_output_cell_exists():
    """
    Check that there is only one output cell.

    Raises
    ------
    Exception
        - If output cell does not exist.
        - If there are two or more output cells.
    """
    driver = selenium_helper.driver
    output_cell_elem_list = driver.find_elements_by_class_name(
        OUTPUT_TEXT_SELECTOR_CLASS_STR)
    if not output_cell_elem_list:
        raise Exception('The cell of the output does not exist.')
    if len(output_cell_elem_list) != 1:
        raise Exception('There are two or more output cells.')


def update_ipynb_test_source_code(source_code):
    """
    Directly update code in JSON of the ipynb file.
    It is difficult to control Jupyter's input to the
    cell via selenium, so use this function.

    Parameters
    ----------
    source_code : str
        Source code to set.
    """
    ipynb_dict = _read_test_ipynb_dict()
    _assert_only_one_code_cell_exists(
        ipynb_dict=ipynb_dict)
    code_cell_idx = _get_ipynb_code_cell_idx(
        ipynb_dict=ipynb_dict)
    ipynb_dict = _replace_ipynb_code_cell(
        ipynb_dict=ipynb_dict, source_code=source_code,
        code_cell_idx=code_cell_idx)
    _save_test_ipynb_dict(ipynb_dict=ipynb_dict)


def _save_test_ipynb_dict(ipynb_dict):
    """
    Save the dictionary data of the test ipynb file.

    Parameters
    ----------
    ipynb_dict : dict
        Dictionary to be saved.
    """
    ipynb_json_str = json.dumps(ipynb_dict)
    with open(TEST_JUPYTER_NOTE_PATH, 'w') as f:
        f.write(ipynb_json_str)


def _read_test_ipynb_dict():
    """
    Read the dictionary data of the test ipynb file.

    Returns
    -------
    ipynb_dict : dict
        Dictionary of loaded data.
    """
    with open(TEST_JUPYTER_NOTE_PATH, 'r') as f:
        ipynb_json_str = f.read()
    ipynb_dict = json.loads(ipynb_json_str)
    return ipynb_dict


def _replace_ipynb_code_cell(ipynb_dict, source_code, code_cell_idx):
    """
    Replace the source code of the code cell of the specified
    index.

    Parameters
    ----------
    ipynb_dict : dict
        Dictionary of notebook data.
    source_code : str
        Source code to set.
    code_cell_idx : int
        The index of the target code cell.

    Returns
    -------
    ipynb_dict : dict
        Dictionary of notebook after replacement.
    """
    cell_dict = ipynb_dict['cells'][code_cell_idx]
    source_code = source_code.strip()
    source_code_line_list = source_code.split('\n')
    for i, source_code in enumerate(source_code_line_list):
        source_code_line_list[i] = source_code + '\n'
    cell_dict['source'] = source_code_line_list
    return ipynb_dict


def _get_ipynb_code_cell_idx(ipynb_dict):
    """
    Get the index of the code cell.

    Parameters
    ----------
    ipynb_dict : dict
        Dictionary of notebook data.

    Returns
    -------
    idx : int
        The index of the code cell.
    """
    idx = 0
    cells_list = ipynb_dict['cells']
    for cell_dict in cells_list:
        if cell_dict['cell_type'] != 'code':
            idx += 1
            continue
        break
    return idx


def _assert_only_one_code_cell_exists(ipynb_dict):
    """
    Check that there is only one code cell in ipynb.

    Parameters
    ----------
    ipynb_dict : dict
        Dictionary of notebook data.

    Raises
    ------
    Exception
        - If the code cell does not exist.
        - If there are multiple code cells.
    """
    code_cell_num = 0
    is_in = 'cells' in ipynb_dict
    if not is_in:
        raise Exception(
            'There is no cell in the notebook.')
    cells_list = ipynb_dict['cells']
    for cell_dict in cells_list:
        if cell_dict['cell_type'] != 'code':
            continue
        code_cell_num += 1

    if code_cell_num == 0:
        raise Exception(
            'There is no code cell in the notebook.')
    if code_cell_num != 1:
        raise Exception(
            'Multiple code cells are not acceptable.')



def _get_test_code_cell_elem():
    """
    Get the WebElement of the form to be used as a test
    code cell.

    Raises
    ------
    Exception
        - If the Jupyter code cell does not exist on the
            current page.
        - If there are multiple cells of code.

    Returns
    -------
    code_cell_elem : selenium.webdriver.remote.webelement.WebElement
        WebElement of code input form.
    """
    _assert_current_page_is_test_notebook()
    code_cell_elem_list = selenium_helper.driver.find_elements_by_css_selector(
        'div.CodeMirror.cm-s-ipython')
    if len(code_cell_elem_list) == 0:
        raise Exception('Could not find any cell for code input. Please check if Jupyter structure has changed.')
    if len(code_cell_elem_list) != 1:
        raise Exception('There are several input cells on the test notebook. Please adjust to only one.')
    code_cell_elem = code_cell_elem_list[0]
    return code_cell_elem


def _assert_current_page_is_test_notebook():
    """
    Check that the page currently open in selenium is a Jupyter
    notebook for testing.

    Raises
    ------
    Exception
        - If webdriver is not running.
        - If the test notebook is not open.
    """
    if selenium_helper.driver is None:
        raise Exception('Webdriver is not running.')
    if selenium_helper.driver.title != TEST_JUPYTER_NOTE_NAME:
        raise Exception('The test notebook is not open.')


def hide_input_cell():
    """
    Hide the input cells.
    """
    _assert_current_page_is_test_notebook()
    driver = selenium_helper.driver
    script = '$(".{input_selector_class_str}").css("display", "none");'.format(
        input_selector_class_str=INPUT_SELECTOR_CLASS_STR
    )
    driver.execute_script(script)


def hide_header():
    """
    Hide the elements such as the menu at the top of the note.
    """
    script = '$("#{header_container_id}").css("display", "none")'.format(
        header_container_id=HEADER_CONTAINER_SELECTOR_ID_STR
    )
    selenium_helper.driver.execute_script(script)

    script = '$("#{menu_bar_container_id}").css("display", "none")'.format(
        menu_bar_container_id=MENU_BAR_CONTAINER_SELECTOR_ID_STR
    )
    selenium_helper.driver.execute_script(script)
