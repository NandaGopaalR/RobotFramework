*** Settings ***

Library    SeleniumLibrary


Resource    ${CURDIR}/../Base/Global_variable.resource

*** Variables ***

*** Keywords ***

CustomClickButton
    [Documentation]    This keyword is used to click on a button and capture a screenshot.
    [Arguments]    ${locator}

    #Wait until the element is visible 
    Wait Until Page Contains Element    ${locator}    ${wait_time}
    #Get the web element using the locator
    ${WebElement}=    Get WebElement    ${locator}
    
    #capture the screenshot of the element
    Capture Element Screenshot    ${WebElement}    screenshot_${TEST NAME}.png
    #click the button
    Click Button    ${WebElement}
    
   