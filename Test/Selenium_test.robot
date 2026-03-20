*** Settings ***
Library             SeleniumLibrary
# The CURDIR is a built-in variable that always points to the directory where the current test case file(.robot) is located.
Variables           ${CURDIR}/../config/Configuration.yaml
Resource            ${CURDIR}/../Resources/Base/Base_Action.resource
Resource            ${CURDIR}/../Resources/Base/Global_variable.resource

Suite Setup         StartCycle
Suite Teardown      EndCycle


*** Variables ***
${Url}              ${CONFIGS.url3}
${browser}          ${CONFIGS.browser}
${WebElement}       //li[@class="menu-item"]/a[@id="nav_automobile"]
${Driverpath}       ${CURDIR}/../drivers/chromedriver.exe


*** Test Cases ***
TestCase1
    [Documentation]    This is a test case to verify the title of the page.
    ${this_test}=    Set Variable    This is a test case to verify the title of the page.
    ${thisvalue}=    Set Variable    This is a test case to verify the title of the page.
    ${var}=    Set Variable    //a[@class="text-black text-size-14 hover:text-lambda-900 leading-relaxed"][@href]
    CustomClickLink    ${var}

    # create new branch and merge to main branch test


*** Keywords ***
StartCycle
    Open Browser    # D:/Automation/RobotFramework_Project/Base/drivers/chromedriver.exe
    ...    ${url}
    ...    ${browser}
    ...    executable_path=${Driverpath}
    Maximize Browser Window
    Sleep    3s

EndCycle
    [Documentation]   This keyword is used to close the browser after the test case execution.
    Close Browser
