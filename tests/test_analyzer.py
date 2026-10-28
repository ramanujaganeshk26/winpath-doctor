import os
import tempfile
import unittest
from winpath_doctor.analyzer import PathAnalyzer, PathEntry
from winpath_doctor.backup import PathBackup


class TestPathDoctor(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.existing_dir = self.tmp_dir.name
        self.non_existing_dir = os.path.join(self.existing_dir, "non_existent_subdir")

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_path_entry_normalize(self):
        normalized = PathEntry.normalize(' "C:\\Foo\\Bar\\" ')
        self.assertEqual(normalized, os.path.normpath("C:/Foo/Bar"))

    def test_duplicate_detection(self):
        path_str = os.pathsep.join([self.existing_dir, self.existing_dir, self.non_existing_dir])
        analyzer = PathAnalyzer(path_str)
        duplicates = analyzer.get_duplicates()
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0][0], 1)

    def test_dead_path_detection(self):
        path_str = os.pathsep.join([self.existing_dir, self.non_existing_dir])
        analyzer = PathAnalyzer(path_str)
        dead = analyzer.get_dead_paths()
        self.assertEqual(len(dead), 1)
        self.assertEqual(dead[0][1], self.non_existing_dir)

    def test_clean_path(self):
        path_str = os.pathsep.join([self.existing_dir, self.existing_dir, self.non_existing_dir])
        analyzer = PathAnalyzer(path_str)
        cleaned = analyzer.clean()
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0], os.path.normpath(self.existing_dir))

    def test_backup_create_and_list(self):
        with tempfile.TemporaryDirectory() as b_dir:
            mgr = PathBackup(storage_dir=b_dir)
            path_file = mgr.create_backup("C:\\bin;D:\\tools", label="test")
            self.assertTrue(os.path.exists(path_file))
            backups = mgr.list_backups()
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0]["label"], "test")


if __name__ == "__main__":
    unittest.main()
