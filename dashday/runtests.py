# Dashday testing
# Designed to be run by Travis CI. Should work for humans too, we suppose. But humans? Bleh.
# Remember to set the DASHDAY_TESTMODE and DASHDAY_DPKEY env-vars before testing.

import tests.configuration, tests.printer, tests.server
import main

try:
    # Run the configuration tests
    tests.configuration.dashdayConfTest()
    print("Dashday.cfg.sample configuration test passed")
    tests.configuration.weatherConfTest()
    print("Weather.cfg.sample configuration test passed")
    tests.configuration.webConfTest()
    print("Web.cfg configuration test passed")
    tests.configuration.dashdaySaveCfgTest()
    print("Test.cfg configuration save test passed")

    # Run printer-related tests with dummy printers
    tests.printer.testSetFont()
    print("Dummy printer font set test passed")
    tests.printer.testPrintText()
    print("Dummy printer text print test passed")
    tests.printer.testPrintImage()
    print("Dummy printer image print test passed")
    tests.printer.testCutPaper()
    print("Dummy printer cut paper test passed")

    # Run the test for the web server
    tests.server.testWebServer()
    print("Internal web server test passed")

    # Finally, run the actual Dashday script - this should be done with the testmode env-var
    main.start()
    print("Main script tests passed")

    # If this all works, congrats - you've managed to not screw something up, which is a miracle!
    print("All tests passed - dashday build tests successful")
except Exception as e:
    print("Tests failed with exception \"" + str(e) + "\" - dashday build tests failed.")
    raise