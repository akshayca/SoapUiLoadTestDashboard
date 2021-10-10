@ECHO OFF

set projectRootFolder=C:\SoapUiLoadTest\TestCase\

set ReportFoler=C:\SoapUiLoadTest\TestResults\

set limit=15
set thread=10

set hour=%time:~0,2%
if "%hour:~0,1%" == " " set hour=0%hour:~1,1%
set timestamp=%date:~-4,4%%date:~-10,2%%date:~7,2%%hour%%time:~3,2%

cd TestResults
mkdir %date:~-4,4%%date:~-10,2%%date:~7,2%%hour%%time:~3,2%

cd /d C:\Program Files\SmartBear\SoapUI-5.6.0\bin

REM Calculator Add

set addLT=loadtestrunner.bat -s"CalculatorSoap TestSuite" -c"Add TestCase" -l"LoadTestAdd" -m%limit% -n%thread% -r -f%ReportFoler%%timestamp% "%projectRootFolder%example-soapui-project.xml"

REM Calculator Divide

set divideLT=loadtestrunner.bat -s"CalculatorSoap TestSuite" -c"Divide TestCase" -l"LoadTestDivide" -m%limit% -n%thread% -r -f%ReportFoler%%timestamp% "%projectRootFolder%example-soapui-project.xml"

REM Calculator Multiply

set multiplyLT=loadtestrunner.bat -s"CalculatorSoap TestSuite" -c"Multiply TestCase" -l"LoadTestMultiply" -m%limit% -n%thread% -r -f%ReportFoler%%timestamp% "%projectRootFolder%example-soapui-project.xml"

REM Calculator Subtract

set subtractLT=loadtestrunner.bat -s"CalculatorSoap TestSuite" -c"Subtract TestCase" -l"LoadTestSubtract" -m%limit% -n%thread% -r -f%ReportFoler%%timestamp% "%projectRootFolder%example-soapui-project.xml"



echo ===================================================================
echo --------------SoapUi Load test execution ----------------------------
echo ===================================================================
echo:

call %addLT%
call %divideLT%
call %multiplyLT%
call %subtractLT%

REM cd /d C:\TestResults

REM python MergeCSVs.py %timestamp%
