# Test suites

pytest cases (not `.air`) — one runner for the whole project. Each suite mirrors
a game area. Cases use page objects from `pixon.pages` and flows from `pixon.flows`.

| Suite | Target | Cases shipped |
|-------|--------|---------------|
| `DailyMission/` | Daily mission (target: 33) | 1 example |
| `HeartSystem/` | Heart system (target: 31) | 1 example |
| `player-profile/` | Player profile, legacy (target: 2) | 1 example |
| `test_framework_selfcheck.py` | base framework, no device | 6 checks |

**Cap:** only 1 example per suite is shipped — the remaining real cases need real
screen crops in `pixon/pages/images/`. Copy an example, swap selectors.

Run: `pytest` (all) · `pytest -m daily_mission` · `pytest Test/test_framework_selfcheck.py` (no device).
