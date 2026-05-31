from __future__ import annotations

from datetime import date, timedelta

from nova.plugins.base import NovaPlugin, PluginManifest, PluginResult


class StudyPlannerPlugin(NovaPlugin):
    manifest = PluginManifest("study_planner", "Create local study plans from topics", ["memory:read"])

    def commands(self) -> dict[str, str]:
        return {"plan": "Create a 7-day study plan from comma-separated topics"}

    def run(self, command: str, argument: str) -> PluginResult:
        if command != "plan":
            return PluginResult(False, f"Unknown study planner command: {command}")
        topics = [t.strip() for t in argument.split(",") if t.strip()] or [argument.strip() or "Revision"]
        today = date.today()
        schedule = []
        for idx in range(7):
            topic = topics[idx % len(topics)]
            schedule.append(
                {
                    "date": str(today + timedelta(days=idx)),
                    "focus": topic,
                    "method": "Read → summarize → active recall → practice questions → review mistakes",
                }
            )
        return PluginResult(True, "Study plan created", {"schedule": schedule})
