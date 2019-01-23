plot playground is a plot library that works on Jupyter and Pandas datasets. Notes: currently developing phase.

# Testing

Please use Windows10 to run the test.

The following libraries are used for testin:

```
$ pip install chromedriver-binary==2.45.0
$ pip install selenium==3.13.0
$ pip install win10toast==0.9
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
