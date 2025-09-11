import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def _force_offscreen_qt_in_ci():
    # Use offscreen when no display is available (e.g., CI/Linux)
    if os.environ.get("CI") == "true" or not os.environ.get("DISPLAY"):
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
