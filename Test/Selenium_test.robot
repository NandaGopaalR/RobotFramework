*** Settings ***
Library    SeleniumLibrary
# The CURDIR is a built-in variable that always points to the directory where the current test case file(.robot) is located.
Variables    ${CURDIR}/../config/defaults.yaml

*** Variables ***
${url}=    ${CONFIGS.url}
${browser}=    ${CONFIGS.browser}

*** Test Cases ***
OpenBrowser1
    SeleniumLibrary.Open Browser    ${url}    ${browser}    alias= myBrowser    options= add_experimental_option("dtach",True)