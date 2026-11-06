# Weekly Client Status Report Generator

A small Python tool for a Technical Program Manager. It reads the **Summary** and **Risks & Issues** tabs of the Task 5 Excel tracker and creates separate weekly reports for Nirmal Finance (Kavach) and Sagar Publications (Ledger).

## How to run

1. Install Python 3.9 or newer. No additional packages are needed.
2. Download or clone this repository and open a terminal in its folder.
3. Run:

```bash
python report_generator.py T5_Project_Tracker.xlsx
```

The tool creates `reports/kavach_weekly_report.md` and `reports/ledger_weekly_report.md`. Open them in any text editor. To choose another output folder, use `--output folder_name`.

## Input

`T5_Project_Tracker.xlsx` is included as an example. The first worksheet contains project summary rows (project, status, milestone, date, main problem). The second contains risks and issues (project, description, probability, impact, owner, action, due date). Keep the same columns and tab order when editing the file.

## Why this helps

Instead of copying project details into two updates each week, I can update the tracker once, run the script, and review the two reports before sending them. The report generator filters issues by project so client information is not mixed.

## AI Prompts Used in Cursor

**Prompt 1 – Error Handling**

"I have built a Python tool that reads an Excel project tracker and generates weekly status reports for Kavach and Ledger. The script is working.

Please review report_generator.py and make one small improvement: if the Excel file is missing, show a clear, user-friendly error message instead of a technical traceback.

Keep the code simple, preserve the existing functionality, and explain what you changed."

## AI-Assisted Improvement

While reviewing the tool in Cursor, I asked AI to improve how the script handles missing Excel files.

Cursor updated the script to show a clear error message instead of a technical traceback.

I tested this using an incorrect filename and then ran the script again with the correct tracker. Both client reports were generated successfully.

## AI Review and Testing

I used Cursor AI to review the report generator and improve its error handling.

The original script could show a technical error when the Excel file was missing. I asked Cursor to make the message easier to understand.

After the change, I tested the script with an incorrect filename and then with the correct Excel tracker. Both client reports generated successfully.

I also checked that Kavach and Ledger risks appeared only in their respective reports.

## Limitations

- Designed for the Task 5 tracker structure, with Summary as the first tab and Risks & Issues as the second.
- Outputs Markdown text; review dates and wording before sending.
- It does not email clients or update the Excel tracker.
