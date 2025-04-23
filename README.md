# Medical Device QA
This tool validates CPAP firmware against saftety-critical requirements for:  
- Pressure control accuracy (ISO 80601-2-70).  
- Alarm thresholds (e.g., apnea detection failure).  
- Risk mitigation per **IEC 62304** (medical device software standard). 

##  Quality Assurance Applications  
- **Automated Regression Testing**: Verify firmware updates don’t violate safety limits.  
- **Fault Injection**: Simulate sensor failures (e.g., pressure sensor drift) to test error handling.  
- **Traceability**: Maps test cases to regulatory requirements (ISO 13485 Sec. 7.3). 

##  Regulatory Standards  
Designed to support compliance with:  
- **ISO 13485:2016** (QMS for Medical Devices)  
- **FDA 21 CFR Part 820** (Quality System Regulation)  
- **IEC 62304** (Medical Device Software Lifecycle)  
