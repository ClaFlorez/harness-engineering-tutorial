import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validator import validate_episode


class ValidatorTests(unittest.TestCase):
    def test_valid_input_is_not_modified(self):
        data = {"title": " Ejemplo ", "script": "a" * 20, "extra": [1]}
        before = copy.deepcopy(data)
        self.assertEqual(validate_episode(data), [])
        self.assertEqual(data, before)

    def test_title_boundaries_and_types(self):
        for title, valid in [("x", True), ("x" * 100, True),
                             ("x" * 101, False), ("   ", False),
                             (None, False), (123, False)]:
            with self.subTest(title=title):
                errors = validate_episode({"title": title, "script": "x" * 20})
                self.assertEqual(errors == [], valid)

    def test_script_boundaries_and_types(self):
        for script, valid in [("x" * 19, False), ("x" * 20, True),
                              ("  " + "x" * 19 + "  ", False),
                              (None, False), ([], False)]:
            with self.subTest(script=script):
                errors = validate_episode({"title": "Título", "script": script})
                self.assertEqual(errors == [], valid)

    def test_tags_are_optional(self):
        self.assertEqual(validate_episode({"title": "Demo", "script": "x" * 20}), [])

    def test_tags_boundaries_and_repeated_values(self):
        for tags, valid in [([], True), (["IA"] * 5, True),
                            (["IA"] * 6, False), ([" IA ", "IA"], True)]:
            with self.subTest(tags=tags):
                data = {"title": "Demo", "script": "x" * 20, "tags": tags}
                before = copy.deepcopy(data)
                self.assertEqual(validate_episode(data) == [], valid)
                self.assertEqual(data, before)

    def test_tags_must_be_a_list(self):
        for tags in [None, "IA", 3, True, {"tag": "IA"}]:
            with self.subTest(tags=tags):
                data = {"title": "Demo", "script": "x" * 20, "tags": tags}
                before = copy.deepcopy(data)
                self.assertTrue(validate_episode(data))
                self.assertEqual(data, before)

    def test_each_tag_must_be_nonempty_text(self):
        for tag in ["", "   ", "\t\n", None, 3, True, [], {}]:
            with self.subTest(tag=tag):
                data = {"title": "Demo", "script": "x" * 20, "tags": ["IA", tag]}
                before = copy.deepcopy(data)
                self.assertTrue(validate_episode(data))
                self.assertEqual(data, before)

    def test_tags_errors_accumulate_with_other_fields(self):
        self.assertEqual(len(validate_episode({"tags": "IA"})), 3)

    def test_missing_fields_accumulate_errors(self):
        self.assertEqual(len(validate_episode({})), 2)

    def test_non_objects_are_rejected(self):
        for data in [[], None, True, 12, "episodio"]:
            with self.subTest(data=data):
                self.assertTrue(validate_episode(data))

    def test_cli_exit_codes_and_machine_readable_output(self):
        program = Path(__file__).resolve().parents[1] / "validator.py"
        cases = [('{"title":"Demo","script":"abcdefghijklmnopqrst"}', 0),
                 ('{"title":"Demo","script":"abcdefghijklmnopqrst","tags":["IA"]}', 0),
                 ('{"title":"Demo","script":"abcdefghijklmnopqrst","tags":[" "]}', 1),
                 ('{"title":""}', 1), ('{invalid', 1),
                 (None, 1), (b'\xff\xfe', 1)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "episode.json"
            for content, code in cases:
                with self.subTest(content=content):
                    if content is None:
                        path.unlink(missing_ok=True)
                    elif isinstance(content, bytes):
                        path.write_bytes(content)
                    else:
                        path.write_text(content, encoding="utf-8-sig")
                    result = subprocess.run(
                        [sys.executable, str(program), str(path)],
                        capture_output=True, text=True, check=False,
                    )
                    self.assertEqual(result.returncode, code, result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertEqual(payload["ok"], code == 0)
                    self.assertIsInstance(payload["errors"], list)
                    self.assertEqual(bool(payload["errors"]), code != 0)


if __name__ == "__main__":
    unittest.main()
