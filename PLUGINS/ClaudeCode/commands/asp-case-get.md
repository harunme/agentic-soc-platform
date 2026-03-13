---
name: asp-case-get
description: Query security case details by case ID
argument-hint: <case_id>
allowed-tools: [ "*" ]
---

Query case details for: {{id}}

Use the MCP tool `get_case` with the provided parameters.

Format the output with:

**Case Overview**

- Case ID and Title
- Severity and Status
- Description
- Created/Updated timestamps

**Associated Alerts**

- Total count
- Summary of key alerts
- Alert types and sources

**Associated Artifacts**

- Total count
- Key entities (IPs, domains, hashes, users)
- Artifact types

**Timeline**

- Event sequence
- Key timestamps

**AI Analysis**

- Any automated analysis results
- Confidence scores
- Recommendations

Present the information in a clear, structured format with appropriate sections.
