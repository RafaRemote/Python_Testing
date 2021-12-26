# gudlift-registration - Quality Assurance Branch

1. Why

    This branch is meant for testing purposes only.

    Tools:
    * [Locust](https://pypi.org/project/locust/) as performance testing tool.
    * [Selenium](https://pypi.org/project/selenium/) as automatic testing tool for functional test.
    * [Coverage](https://pypi.org/project/coverage/) as code coverage measurement tool.

2. Installation

    | Installation Short Summary            | Folder |
    |---------------------------------------|--------|
    | ```pip install -r requirements.txt``` | root   |

3. Testing

    Code coverage measurement.

    | Coverage               | Folder |
    |------------------------|--------|
    | ```pytest --cov=.```   | root   |

    Selenium Functional test will be be also run with this above command, so the coverage will also include the result of this test.

    Performance measurement.

    | Locust without webinterface                                                    | Folder                  |
    |--------------------------------------------------------------------------------|-------------------------|
    | ```locust -f locustfile.py -H http://127.0.0.1:5000/ -u 6 -r 1 --headless```   | tests/performance_tests |

    | Locust with    webinterface                                                    | Folder                  |
    |--------------------------------------------------------------------------------|-------------------------|
    | ```locust -f locustfile.py -H http://127.0.0.1:5000/ -u 6 -r 1 --autostart```  | tests/performance_tests |

    [Translation](https://docs.locust.io/en/stable/configuration.html):
    * -f: filename
    * -H: host
    * -u: users
    * -r: rate (spawn rate)
    * --autostart: runs immediately with web UI
    * --headless: runs immediately without the web UI

    Be Careful to be in the good folder to run locust, you need to run Locust from where ```locustfile.py``` is located.
