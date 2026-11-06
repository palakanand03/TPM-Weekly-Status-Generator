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

## Example AI prompts used to guide the solution

- "Create a small Python tool that reads my Task 5 Excel tracker and produces separate weekly status reports for Kavach and Ledger. Keep it simple and easy to run."
- "Include each project's RAG status, next milestone and date, main problem, and its own risks with owners, actions, and due dates."
- "Make the tool work without third-party Python libraries and add a README with run instructions."

**Prompt disclosure:** These are representative prompts for this AI-assisted build. If you use Claude Code or Cursor yourself, replace them with the exact prompts from your session before submission.

## AI error and correction (verified during review)

**Issue checked:** A report generator could accidentally put Ledger risks in the Kavach client report (or vice versa) if it reads every risk row without filtering by project.

**Correction:** Filter the risks using `row['Project'] == project` before generating each report. I checked the resulting files: the Kavach report contains only Kavach risks and the Ledger report contains only Ledger risks. This is a verified safeguard, not a claim that a separate Claude/Cursor run produced the error. If the assignment requires an actual AI mistake, document one you encounter while using your chosen coding assistant.

## Limitations

- Designed for the Task 5 tracker structure, with Summary as the first tab and Risks & Issues as the second.
- Outputs Markdown text; review dates and wording before sending.
- It does not email clients or update the Excel tracker.
