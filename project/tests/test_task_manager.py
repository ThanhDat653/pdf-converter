import unittest
from pathlib import Path

from core.task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_build_output_path_has_timestamp_and_suffix(self) -> None:
        output = TaskManager.build_output_path(Path("/tmp/output"), "input file.pdf", "docx")
        self.assertEqual(output.parent, Path("/tmp/output"))
        self.assertEqual(output.suffix, ".docx")
        self.assertTrue(output.name.endswith("_input_file.docx"))


if __name__ == "__main__":
    unittest.main()
