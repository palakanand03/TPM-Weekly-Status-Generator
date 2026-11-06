"""Generate client-specific Markdown weekly reports from the Task 5 Excel tracker.
Uses Python's standard library; no packages to install.
"""
import argparse
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
COL_RE = re.compile(r'^([A-Z]+)')
CLIENTS = {'Kavach': 'Nirmal Finance', 'Ledger': 'Sagar Publications'}


def read_excel(path):
    """Read first two worksheets in a simple .xlsx without external dependencies."""
    with zipfile.ZipFile(path) as archive:
        shared = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
            shared = [''.join(t.text or '' for t in si.findall('.//x:t', NS))
                      for si in root.findall('x:si', NS)]
        sheets = []
        for index in (1, 2):
            root = ET.fromstring(archive.read(f'xl/worksheets/sheet{index}.xml'))
            data = []
            for row in root.findall('.//x:sheetData/x:row', NS):
                values = {}
                for cell in row.findall('x:c', NS):
                    col = COL_RE.match(cell.attrib['r']).group(1)
                    value_node = cell.find('x:v', NS)
                    inline = cell.find('x:is', NS)
                    value = value_node.text if value_node is not None else ''
                    if cell.get('t') == 's' and value:
                        value = shared[int(value)]
                    elif inline is not None:
                        value = ''.join(t.text or '' for t in inline.findall('.//x:t', NS))
                    values[col] = value or ''
                if values:
                    data.append(values)
            if not data:
                raise ValueError(f'Worksheet {index} is empty')
            headers = data[0]
            sheets.append([{headers[col]: val for col, val in row.items() if col in headers}
                           for row in data[1:]])
        return sheets


def pick(row, *names):
    for name in names:
        if name in row:
            return str(row[name]).strip()
    return ''


def generate(summary, risks, project):
    client = CLIENTS[project]
    status = pick(summary, 'Status')
    milestone = pick(summary, 'Next milestone')
    date = pick(summary, 'Date (scenario week)', 'Date')
    problem = pick(summary, 'Main problem')
    lines = [f'# Weekly Project Update — {client}', '', f'**Project:** {project}',
             f'**Status:** {status}', f'**Next milestone:** {milestone} ({date})', '',
             '## Current situation', problem, '', '## Risks and actions']
    if not risks:
        lines.append('No risks or issues listed in the tracker.')
    for item in risks:
        description = pick(item, 'Risk / issue description', 'Description')
        action = pick(item, 'Action / mitigation', 'Action')
        owner = pick(item, 'Owner')
        due = pick(item, 'Due (scenario week)', 'Due date')
        lines.append(f'- **{description}** — {action} (Owner: {owner}; Due: {due})')
    lines += ['', '## Next update', 'We will share progress against the milestone and any changes to the risks above.', '',
              '_Generated from the Task 5 tracker. Please review before sending to the client._', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Create weekly client updates from Task 5 tracker')
    parser.add_argument('tracker', type=Path, help='Path to T5_Project_Tracker.xlsx')
    parser.add_argument('--output', type=Path, default=Path('reports'), help='Output folder')
    args = parser.parse_args()
    try:
        summaries, issues = read_excel(args.tracker)
        args.output.mkdir(parents=True, exist_ok=True)
        for project in CLIENTS:
            matching = [row for row in summaries if pick(row, 'Project') == project]
            if len(matching) != 1:
                raise ValueError(f'Expected one Summary row for {project}; found {len(matching)}')
            relevant = [row for row in issues if pick(row, 'Project') == project]
            path = args.output / f'{project.lower()}_weekly_report.md'
            path.write_text(generate(matching[0], relevant, project), encoding='utf-8')
            print(f'Created {path} ({len(relevant)} risks/issues)')
    except FileNotFoundError:
        print(f'Error: Could not find the Excel file "{args.tracker}".', file=sys.stderr)
        print('Check the file path and try again.', file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
