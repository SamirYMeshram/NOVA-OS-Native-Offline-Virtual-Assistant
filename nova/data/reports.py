from __future__ import annotations
import json

class DataReportBuilder:
    def markdown(self, profile: dict) -> str:
        lines = [f"# Data Profile", f"Path: `{profile.get('path')}`", ""]
        if 'rows_sampled' in profile:
            lines.append(f"Rows sampled: **{profile['rows_sampled']}**")
            lines.append(f"Duplicate rows in sample: **{profile.get('duplicates_in_sample', 0)}**")
            lines.append("\n## Columns")
            for name, info in profile.get('columns', {}).items():
                lines.append(f"- **{name}**: {info}")
        else:
            lines.append('```json')
            lines.append(json.dumps(profile, indent=2))
            lines.append('```')
        return '\n'.join(lines)
