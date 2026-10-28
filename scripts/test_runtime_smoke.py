import unittest
from runtime_smoke import validate_hello, validate_shutdown

class RuntimeSmokeTest(unittest.TestCase):
    def test_valid_response(self):
        validate_hello({"code": 0, "data": {"framework": "Neton", "message": "Welcome to Neton", "version": "test"}})

    def test_invalid_response(self):
        for value in ({}, {"code": 1}, {"code": 0, "data": {}}):
            with self.assertRaises(RuntimeError):
                validate_hello(value)

    def test_old_binary_cannot_pass_candidate_check(self):
        with self.assertRaises(RuntimeError):
            validate_hello({"code": 0, "data": {"framework": "Neton", "message": "Welcome to Neton", "version": "old"}}, "new")

    def test_failed_exit_and_leaked_port_fail_closed(self):
        for code, listening in ((1, False), (0, True), (-9, False)):
            with self.assertRaises(RuntimeError):
                validate_shutdown(code, listening)
        validate_shutdown(0, False)

if __name__ == "__main__":
    unittest.main()
