import unittest
import rendur

class TestTemplateFunctions(unittest.TestCase):
	def test_include( self ):
		r = rendur.Create()
		r.assign("planet", "World")
		ret = r.display( r"examples/include1" )
		self.assertEquals( ret, """Before the include
Hello World!
After the include""")