import unittest
from script1 import sshcmd

class TestStringMethods(unittest.TestCase):

    def test_free(self):
        self.assertTrue("total" in script1.sshcmd("161.3.160.65", 22, "interfadm", "Projet654!", "free"))
    def test_ps(self):
        self.assertTrue("CMD" in script1.sshcmd("161.3.160.65", 22, "interfadm", "Projet654!", "ps"))
    def test_vmstat(self):
        self.assertTrue("memory" in script1.sshcmd("161.3.160.65", 22, "interfadm", "Projet654!", "vmstat"))


if __name__ == '__main__':
    unittest.main()
