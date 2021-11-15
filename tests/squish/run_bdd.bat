rem This assumes Squish is installed in the default location (c:\users\<current user>\squish)
set SQUISHPATH=%userprofile%\Squish
set SQUISH_SERVER_HOST=127.0.0.1
set SQUISH_SERVER_PORT=4322
set TESTSUITE=%~dp0\suite_easyDiff_BDD
set REPORTPATH=%~dp0\report
set PYTHONPATH=%userprofile%\Squish\python3

cd %SQUISHPATH%\bin

squishrunner --host %SQUISH_SERVER_HOST% --port %SQUISH_SERVER_PORT% --testsuite %TESTSUITE% --reportgen xml3,%REPORTPATH%/report.xml

cd %REPORTPATH%

%PYTHONPATH%\python.exe %SQUISHPATH%\examples\regressiontesting\squishxml3html.py --dir HTMLReports report.xml\*.xml

rem final report location
rem HTMLReports\index.html

cd %TESTSUITE%\..

