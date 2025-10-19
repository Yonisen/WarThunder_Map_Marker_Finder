import unittest
import sys

sys.path.append('distance/code')


class TestApp(unittest.TestCase):

    def test_imports(self):
        """Test that all main application modules can be imported without errors."""
        try:
            import distance.miniKarta
            import distance.settings
            import distance.code.distanceFinder
            import distance.code.printResults
            import distance.code.scale
            import distance.code.signal1
            import distance.code.signal3
        except ImportError as e:
            self.fail(f"Failed to import one or more modules: {e}")


if __name__ == '__main__':
    unittest.main()
