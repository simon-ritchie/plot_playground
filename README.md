PlotPlayground is a plot library that works on Jupyter and Pandas datasets. This is for making a little unusual plot and playing.

**Notes**: currently developing phase.

# Comparability notes

- It is compatible with Python 3.4 or later version.
- The browser is compatible mainly with Chrome. IE and Edge are not supported. However, Edge will change depending on Chromium transition in future version upgrade.

# Installing

```
$ pip install plot_playground
```

# Examples

## Storytelling simple line date series plot

- This plot is inspired by the wonderful book [Storytelling with Data: A Data Visualization Guide for Business Professionals](https://www.amazon.com/Storytelling-Data-Visualization-Business-Professionals/dp/1119002257/).
- It is useful when you want to show where you should tell in a short time.

![img](https://github.com/simon-ritchie/plot_playground/blob/master/documents/readme/storytelling_simple_line_date_series_plot_white.png)

![img](https://github.com/simon-ritchie/plot_playground/blob/master/documents/readme/storytelling_simple_line_date_series_plot_black.png)

\>\> [More defail and document](https://nbviewer.jupyter.org/github/simon-ritchie/plot_playground/blob/master/documents/storytelling_simple_line_date_series_plot/document.html)

# Colaboratory and Kaggle Kernel

PlotPlayground also supports Google Colaboratory and Kaggle Kernel. Even in these environments you can install with the pip command.

![img](https://github.com/simon-ritchie/plot_playground/blob/master/documents/readme/on_google_colab.png)

Notes: **To use it on Kaggle Kernel, you need to switch the menu setting to "Internet Connected" and execute the pip command.**

![img](https://github.com/simon-ritchie/plot_playground/blob/master/documents/readme/on_kaggle_kernel.png)

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
