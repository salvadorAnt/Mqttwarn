import os
import sys
from pathlib import Path

import pytest


def get_mqttwarn_path():
    return Path(sys.executable).parent / Path("mqttwarn")


def test_command_dump_config(capfd):

    command = "{} make-config".format(get_mqttwarn_path())

    os.system(command)
    stdout = capfd.readouterr().out

    assert 'mqttwarn example configuration file "mqttwarn.ini"' in stdout, stdout


def test_command_dump_samplefuncs(capfd):

    command = "{} make-samplefuncs".format(get_mqttwarn_path())

    os.system(command)
    stdout = capfd.readouterr().out

    assert '# mqttwarn example function extensions' in stdout, stdout


def test_command_standalone_plugin(capfd):

    # FIXME: Make it work on Windows.
    if sys.platform.startswith("win"):
        raise pytest.xfail("Skipping test, fails on Windows")

    command = """{} --plugin=log --options='{}'""".format(get_mqttwarn_path(), '{"message": "Hello world", "addrs": ["crit"]}')

    os.system(command)
    stderr = capfd.readouterr().err

    assert 'Successfully loaded service "log"' in stderr, stderr
    assert 'Hello world' in stderr, stderr
    assert 'Plugin response: True' in stderr, stderr
