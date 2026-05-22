 Collecting data from the site and validating it securely.

                   EXPLANATION
It is a defensive, regex based Python program which processes raw text log data sent back from an external API. It safely validates incoming data, buffers popular injection flaws and pulls out the essential attributes of structured data into a clean JSON format.

       EXTRACTED DATA AND REGEX BREAKDOWN

Validation rules for email addresses (ALU-specific):Validation rules for email addresses (ALU-specific):
   - *Regex Pattern:* `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   - Logic - Captures standard email formats. It then uses conditional filters to categorize valid addresses by the official ALU domain in the address line into one of three custom categories: `official`, `alumni`, or `si`.

2. Credit Card Numbers (Sensitive Data Handling)
   - *Regex Pattern:* `\b(?:\d[ -]*?){13,16}\b`
   - Logic: Recognizes 13- to 16-digit arrays of numbers, frequently separated with a space or hyphen, found on production payment gateways.

3. **URLs**
   - *Regex Pattern:* `https?://[a-zA-Z0-9./?=-]+`
   Logics: Collects production endpoints via both encrypted (`https`) and unencrypted (`http`) protocol handlers.

4. **Currency Amounts**
   - *Regex Pattern:* `\$[0-9,]+\.[0-9]{2}`
   - Logic: Matches standard financial representations beginning with a dollar symbol with thousands (commas) and specific decimal cents.



Security considerations & defensive implementations.

To follow sensitive data handling rules, credit card numbers are also stripped of delimiters and masked (XXXX-XXXX-XXXX-Last4) before being persisted to disk, reducing exposure risks in telemetry outputs.
Strings extracted are checked for abnormalities in their structure (Input Sanitization / Injection Mitigation). HTML character entities such as script indicators (`<script>`, `>`, `<`) are automatically stripped of the specific item to prevent downstream components from being vulnerable to Cross-Site Scripting (XSS).
All collections remove duplicate entries so as to not inflate the log arrays.


How to Run the Program

## Prerequisites
A Python 3.x environment installed in your environment.

### Execution Steps
1. Copy your unformatted API logs to the input file provided:
   `input/raw-text.txt`
   
2. Change to your workspace directory, switch to the source folder and execute the execution script:
   ```bash
   cd src
   python main.py