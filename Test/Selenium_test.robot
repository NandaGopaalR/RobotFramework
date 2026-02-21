*** Settings ***
Library    SeleniumLibrary
# The CURDIR is a built-in variable that always points to the directory where the current test case file(.robot) is located.
Variables    ${CURDIR}/../config/Configuration.yaml
Resource    ${CURDIR}/../Resources/Base/Base_Action.resource
Resource    ${CURDIR}/../Resources/Base/Global_variable.resource

Suite Setup    StartCycle
Suite Teardown   EndCycle
*** Variables ***
${url}=    ${CONFIGS.url2}
${browser}=    ${CONFIGS.browser}
${WebElement}=    //li[@class="menu-item"]/a[@id="nav_automobile"]
*** Keywords ***
StartCycle
    [Documentation]
    Open Browser    ${url}    ${browser}    executable_path=D:/Automation/RobotFramework_Project/Base/drivers/chromedriver.exe
    Maximize Browser Window
    Sleep    3s

EndCycle
    [Documentation]   This keyword is used to close the browser after the test case execution.
    Close Browser

*** Test Cases ***
Test Case 1
  [Documentation]    This is a test case to verify the title of the page.
  ${var}    Set Variable    value
  CustomClickButton   ${WebElement}
  # create new branch and merge to main branch test
