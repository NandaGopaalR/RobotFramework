*** Settings ***
Documentation       Resource file containing XPath and CSS locators for form submission tests.


*** Variables ***
${form_subit_user}=               //label[@for="usr"]
${form_subit_comment}=            //label[@for="comment"]
${form_subit9n_button}=             //input[@type="button"]
${form_subit_button_submit}=      //input[@type="button" and @value="submit"]
${form_subit_validation}=         //span[@class="title-validation validation-error"]
${this_click}=                      //input[@type="test"]
${this_issue}=                   //get
${test_b1ad_cas2e2}=              //get
${dfdf}=    css:sdff

*** Keywords ***
TestTest
    [Arguments]    
    ...    ${arg1}    ${age}   ${age1}    
    ...    ${age5}    ${age6}
    Log    ${arg1}
    Log    ${age}
    Log    ${age1}
    Log    ${age5}
    Log    ${age6}



