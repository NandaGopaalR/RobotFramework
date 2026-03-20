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
Exploring the directory command
    Create Directory    path=DirectoryForTesting
    Create Directory    path=DirectoryForTesting/SubDirectory1/Test1
    Create Directory    path=DirectoryForTesting/SubDirectory1/Test2
    Create File    path=DirectoryForTesting/SubDirectory1/Test1/TestFile1.txt    content=This is a test file.

    File Should Exist    DirectoryForTesting/SubDirectory1/Test1/TestFile1.txt
    ${files}=    List Directory    DirectoryForTesting/SubDirectory1
    Log    ${files}
    File Should Not Be Empty    path=DirectoryForTesting/SubDirectory1/Test1/TestFile1.txt
    ${FileContent}=    Get File    DirectoryForTesting/SubDirectory1/Test1/TestFile1.txt    encoding=UTF-8
    Log    ${FileContent}


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

