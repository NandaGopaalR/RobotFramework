*** Settings ***
# Library resource file for the browser library test cases
Library             Browser    # This library is used to perform the browser action in robot framework
Library             Collections    # This library is used to create the list and dictionary in robot framework
Library             OperatingSystem    # This library is used to explore the directory command in robot framework
# Variables resource file for the browser library test cases
Variables           ${CURDIR}/../config/Configuration.yaml
# Resource file for the browser library test cases
Resource            ${CURDIR}/../Resources/Base/Gloable_Variables.resource

# Test and Suite setup and teardown for the browser library test cases
Suite Setup         StartSuite
Suite Teardown      EndSuite
Test Setup          StartTest
Test Teardown       EndTest


*** Test Cases ***
FillForm
    # New Browser    chromium    headless=${Headless}
    # New Page    ${CONFIGS.url3}
    # Set Viewport Size    1920    1200

    # GO to the Ajaz Form Submit Page
    ${Ele}=    Get Element By    Text    Ajax Form Submit
    Click    ${Ele}
    # verify the lable text
    Get Text    //label[@for="usr"]    ==    Name:
    Get Text    //label[@for="comment"]    ==    Message:
    # click submit button
    Wait For Elements State    //input[@type="button"]    visible
    Click    selector=//input[@type="button" and @value="submit"]
    # verify the mandatory field validation
    Get Text    //span[@class="title-validation validation-error"]    ==    *
    # fill the form
    Click    selector=//div[@class="form-group"]//input[@type="text"]
    Fill Text    selector=//div[@class="form-group"]//input[@type="text"]    txt=Gopaal

    Click    selector=//div[@class="form-group mt-20 mb-20"]//textarea[@id="description"]
    Fill Text
    ...    //div[@class="form-group mt-20 mb-20"]//textarea[@id="description"]
    ...    txt=This is good news now i am able to add my comment

    # click submit button
    Click    selector=//input[@type="button" and @value="submit"]
    Get Text    //div[@id="submit-control"]    ==    Ajax Request is Processing!
    Take Screenshot

ShadowHost
    # New Browser    chromium    headless=${Headless}
    # New Page    ${CONFIGS.url3}
    # Set Viewport Size    1920    1200

    # GO to the Shadow Dom Submit Page
    ${Ele}=    Get Element By    Text    Shadow DOM
    Click    ${Ele}

    # Click    //div[@id="shadow_host"]//div//input[@type="text"]
    Fill Text    css=#shadow_host >> css=input[placeholder="Name"]    txt=Gopaal

    # Click    //div[@id="shadow_host"]/div/input[@type="email"]
    Fill Text    css=#shadow_host >> css=input[placeholder="Email"]    txt=gopal@co.in

    Get Property    css=#shadow_host >> css=input[type="range"]    value    ==    50

    Take Screenshot

BootStrapDualListDemo
    # GO to the Shadow Dom Submit Page
    ${Ele}=    Get Element By    Text    Bootstrap List Box
    Click    ${Ele}

    FOR    ${V}    IN    ${Ele}
        Log    ${V}
    END

    # Verify the all items in the left list are selected by adding active class
    @{Dictlist}=    CheckActiiveClass
    ...    //div[@class="well text-right"]//ul[@class="list-group sp_list_group mb-20 mt-10"]//li
    ...    AllInActive

    # Click on the all items in left list
    Click    selector=//div[@class="well text-right"]//a[@title="select all"]

    # Verify the all items in the left list are selected by adding active class
    CheckActiiveClass
    ...    //div[@class="well text-right"]//ul[@class="list-group sp_list_group mb-20 mt-10"]//li
    ...    AllActive

    # CLick on the buttoon to move the all items form left list to right list
    Click
    ...    selector=//button[@class="block mx-auto border border-black mt-10 px-10 py-2 rounded text-black btn btn-default btn-sm move-right"]


*** Keywords ***
StartSuite
    New Browser    chromium    headless=${Headless}

StartTest
    New Page    ${CONFIGS.url3}
    Set Viewport Size    1920    1200

EndTest
    Close Page    ${CONFIGS.url3}

EndSuite
    Close Browser

CheckActiiveClass
    [Documentation]    This keyword will check the active class is present or not in the list of element and based on the check method it will verify the status of all the element in the list
    ...   ${ElementLocator}  (Element Locator)
    ...   ${CheckMethod}  (AllActive/AllInActive)n
    [Arguments]    ${ElementLocator}    ${CheckMethod}
    ${Ele}=    Get Elements    ${ElementLocator}
    ${Count}=    Get Length    ${Ele}
    &{NewDict}=    Create Dictionary
    @{ThisList}=    Create List
    Create List
    FOR    ${Item}    IN    @{Ele}
        ${Class}=    Get Attribute    ${Item}    class
        ${Status}=    Run Keyword And Ignore Error
        ...    Should contain    ${Class}    active
        ${Text}=    Get Text    ${Item}
        ${NewDict}=    Create Dictionary    ClassName=${Class}    Status=${Status}    text=${Text}
        Append To List    ${ThisList}    ${NewDict}
    END

    IF    '${CheckMethod}' == 'AllActive'
        FOR    ${List}    IN    @{ThisList}
            # FOR    ${key}    IN    @{List.keys()}
            Should Contain    ${List['Status']}    PASS
            # END
        END
    ELSE IF    '${CheckMethod}' == 'AllInActive'
        FOR    ${List}    IN    @{ThisList}
            # FOR    ${key}    IN    @{List.keys()}
            Should Contain    ${List['Status']}    FAIL
            # END
        END
    END

    RETURN    ${NewDict}
