*** Settings ***
# Test setup and libraries
Documentation     Alarm validation tests for CPAP firmware
...              Validates apnea detection meets ISO 80601-2-70 requirements
Library          ${EXECDIR}/scripts/alarm_testing.py

*** Variables ***
# Alarm threshold parameters (all values in seconds)
${APNEA_THRESHOLD}       10.0     # Standard threshold in seconds
${TEST_DURATION_ABOVE}    10.1     # Above threshold (10.0 + 0.1)
${TEST_DURATION_BELOW}    9.9      # Below threshold (10.0 - 0.1)

*** Test Cases ***
Apnea Alarm Triggers Correctly
    [Documentation]    Verify alarm triggers when apnea exceeds threshold
    ...                (ISO 80601-2-70 Section 201.12)
    ${result}=    Test Apnea Alarm    ${TEST_DURATION_ABOVE}    ${True}
    Should Be True    ${result}    Alarm failed to trigger for apnea event

No False Alarm Below Threshold
    [Documentation]    Verify no false alarm when below threshold
    ...                (IEC 62304 Section 5.7)
    ${result}=    Test Apnea Alarm    ${TEST_DURATION_BELOW}    ${False}
    Should Be True    ${result}    False positive apnea alarm detected