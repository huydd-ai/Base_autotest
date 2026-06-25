# pixon — puzzle game test framework (Airtest + pytest)

UI automation for a Unity puzzle game on **LDPlayer**. Page Object Model, Airtest
image-template matching, pytest runner. Layered: `Test → flows → pages → common`,
with `common`/`airtouch_fast` forbidden from importing upward (enforced by import-linter).

## Setup
```bash
pip install -r requirements.txt          # runtime
pip install -r requirements-dev.txt      # + pylint/mypy/import-linter
pip install -e .                         # make `pixon` importable
cp .env.example .env                      # optional; edit values
```

## Add a game (the whole point)
The framework is game-pluggable: shared page objects, **per-game profile + image pack**.
Adding a game touches no framework code.

```bash
adb connect 127.0.0.1:5555                          # LDPlayer instance 0
adb shell pm list packages | findstr <name>         # find the package

python scripts/add_game.py mygame --package com.foo.bar
# -> creates games/mygame/game.json + games/mygame/images/
```
Then crop real screens into `games/mygame/images/` as PNGs, referenced by bare name
(`main_menu`, `btn_play`, `board`, ...) in page objects/tests, and run:
```bash
GAME=mygame pytest          # Windows: set GAME=mygame && pytest
```
`GAME` selects the profile (default `demo`). `DEVICE_URI`/`APP_PACKAGE` env vars
override the profile. A missing/half-set game fails loud at the `device` fixture.

## Run
```bash
pytest                                  # all suites
pytest -m daily_mission                 # one suite
pytest Test/test_framework_selfcheck.py # no device needed
lint-imports                            # check the layering contract
```

## Layout
```
pixon/
  common/      actions, ocr, log, config, sync, adb_utils, *_watchdog   (lowest layer)
  flows/       test_flow — orchestration ABOVE pages (lifted out of common)
  pages/       Page Object Model (+ components/, popup/, images/)
  custom/      empty on purpose (YAGNI until a real override exists)
  airtouch_fast/  minitouch/minicap fast input (fallback: airtest touch)
games/         per-game profiles: games/<name>/game.json + images/   (demo ships)
scripts/       add_game.py — scaffold a new game profile
Test/          pytest suites (DailyMission, HeartSystem, player-profile) + self-check
```

### Deviations from the reference tree (deliberate)
- `wrappers.py` is a **facade** re-exporting `actions`/`ocr`/`log` (was a god module).
- `test_flow` lives in **`flows/`**, not `common/` — breaks the `common→pages→common` cycle.
- Cases are **pytest**, not `.air` — one runner. `.air`/AirtestIDE deferred.
- `ocr`, `adb_utils.cheat`, watchdog scans, minitouch socket are **stubs** — no game code yet.

## Concurrency
`common/sync.py` is the seam: every gesture takes `input_lock()`; watchdog threads
register so a test can `with suppress_popups(): ...` while asserting on a dialog.

## Infra vs code failures
`infra_guard` (autouse) wraps every test. adb/emulator drop (not an `assert`) →
evidence to `results/drops.jsonl` + screenshot, reported **skipped** (`INFRA DROP`).
Real assertion failures still fail normally.
