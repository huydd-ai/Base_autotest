# Puzzle game test harness (Airtest + pytest)

Image-template UI tests for a Unity puzzle game running on **LDPlayer**.
Airtest is used as-is (image recognition + touch); pytest organizes and runs cases.

## Setup
```bash
pip install -r requirements.txt
```

## Connect LDPlayer
1. Start your LDPlayer instance and install the game APK.
2. Connect adb (instance 0 default port):
   ```bash
   adb connect 127.0.0.1:5555
   adb devices            # should list 127.0.0.1:5555
   ```
   Other instances use 5557, 5559, ... — update `DEVICE_URI` accordingly.
3. Find the package name and set it:
   ```bash
   adb shell pm list packages | findstr <part-of-name>
   set APP_PACKAGE=com.yourcompany.puzzle      # Windows; export on Linux/mac
   ```

## Add your screenshots
Crop real game screens into `images/` as PNGs: `main_menu.png`, `btn_play.png`,
`board.png` (these are the names `tests/test_puzzle_smoke.py` expects). Add more
crops and reference them by bare name in new tests.

## Run
```bash
pytest                 # all tests
pytest -k smoke        # just the smoke case
pytest tests/test_helpers_pathing.py   # no device needed
```

## Layout
Base code lives in `base/`; root holds only this README, `requirements.txt`, `pytest.ini`.

| Path | Purpose |
|------|---------|
| `base/config.py` | `DEVICE_URI`, `APP_PACKAGE`, dirs — all env-overridable |
| `base/conftest.py` | fixtures: connect device once, start/stop app, `infra_guard` |
| `base/actions.py` | ONE import for all actions (`tap`/`swipe`/`wait_for`/...) + raw airtest re-exports + `is_infra_error` |
| `base/tests/` | your testcases; copy `test_puzzle_smoke.py` as the pattern |
| `base/images/` | template PNG crops you supply |
| `base/results/` | infra-drop evidence (jsonl + screenshots); gitignored |

## Infra vs code failures
`infra_guard` (autouse) wraps every test. If a test dies because adb/the emulator
dropped (not its own `assert`), it's saved to `results/drops.jsonl` + a screenshot
and reported as **skipped** (`INFRA DROP ...`) — so device flakiness never shows up
as a red code failure. Real assertion failures still fail normally.
