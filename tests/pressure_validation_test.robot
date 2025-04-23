*** Settings ***
Documentation     Pressure validation test cases for CPAP firmware.
Library           ${EXECDIR}/scripts/pressure_validator.py
Library           ${EXECDIR}/scripts/influx_logger.py

*** Variables ***
${SAFE_PRESSURE}       12.5
${UNSAFE_PRESSURE}     22.0
${DEFAULT_TARGET}      12.0

*** Test Cases ***
Normal Pressure Range Validation
    [Documentation]    Validates pressure within safe 4–20 cmH2O range per ISO 80601-2-70.
    ${result}=    Validate Pressure    ${SAFE_PRESSURE}    ${DEFAULT_TARGET}
    Should Be Equal    ${result}    ${True}

Critical Pressure Threshold Violation
    [Documentation]    Fails when pressure exceeds safe tolerance range.
    ${result}=    Validate Pressure    ${UNSAFE_PRESSURE}    ${DEFAULT_TARGET}
    Should Be Equal    ${result}    ${False}