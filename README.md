PlotPlayground is a plot library that works on Jupyter and Pandas datasets. This is for making a little unusual plot and playing.

**Notes**: currently developing phase.

# Comparability notes

- It is compatible with Python 3.4 or later version.
- The browser is compatible mainly with Chrome. IE and Edge are not supported. However, Edge will change depending on Chromium transition in future version upgrade.

# Testing

Please use Windows10 to run the test.

The following libraries are used for testing:

```
$ pip install chromedriver-binary==2.45.0
$ pip install selenium==3.13.0
$ pip install win10toast==0.9
$ pip install Pillow==5.2.0
$ pip install jupyter==1.0.0
$ pip install notebook==5.5.0
$ pip install opencv-python==4.0.0.21
$ pip install numpy==1.14.5
$ pip install voluptuous==0.11.5
# pip install nose==1.3.7
```

After installing the library, the test is executed with the following command:

```
$ python run_tests.py
```

To perform tests on individual module units, execute as shown in the following command:

```
$ python run_tests.py --module_name plot_playground.tests.test_selenium_helper
```

**If the coordinates of the test screenshot do not match:**

Maybe the magnification of the screen resolution is other than 100%. Please try setting 100% once.
