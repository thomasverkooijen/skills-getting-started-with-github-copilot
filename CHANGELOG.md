# Changelog

All notable changes to this project are documented in this file.

## 2025-12-16 — accelerate-with-copilot

- Added six new activities: 2 sports (`Soccer Team`, `Swimming Club`), 2 artistic (`Photography Club`, `Music Ensemble`) and 2 intellectual (`Math Olympiad`, `Robotics Club`).
- Updated the UI to show participants per activity in activity cards.
- Added remove (unregister) button next to each participant; clicking it calls a new `DELETE /activities/{activity_name}/participants?email=...` endpoint.
- Improved styling for participants list (hidden bullets, inline remove button, hover states).
- Fixed a bug in `signup_for_activity` where a variable shadowing prevented correct signups — now tests cover signup behavior.
- Added pytest-based tests (`tests/test_app.py`) and updated `requirements.txt` to include `pytest`, `requests`, and `httpx`.

These changes improve the interactivity of the activities UI and add test coverage for core API flows.
