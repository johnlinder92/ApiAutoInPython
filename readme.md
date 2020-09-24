What you need to run the tests:

You need a Virtual environment with python. So download python. I am using the latest verison of python 3.9, but some older versions will probably work to.

You allso need the dependencies specified in requirements.txt.
If your environment doesnt download them automatically for you, then you need to write
- pip install pytest

Then right click the imports of code and install these code packages in the start of thetests.py

Now you should be set to run the tests from command line.

Here are some examples of what you could write:
- pytest thetests.py (normal run)
- pytest thetests.py -m command (runs all tests with the pytest command marker on them(which is all commands))
- pytest thetests.py -m queries (the same for all queires)
- pytest thetests.py --junitxml=C:\reports\junitxmlreport.xml (produces a junitxml report stored in specified folder)
