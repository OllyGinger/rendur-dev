import unittest
import rendur

class TestBasicRenders(unittest.TestCase):
	def test_basic_render( self ):
		r = rendur.Create()
		r.assign("planet", "World")
		ret = r.display( r"examples/basic" )
		self.assertEquals( ret, "Hello World!")
	
	def test_basic_render2( self ):
		r = rendur.Create()
		r.assign("hello", "Hello")
		r.assign("world", "world")
		ret = r.display( r"examples/basic2" )
		self.assertEquals( ret, """Hello world!
Hello world
I have no tags :(""")

	def test_basic_render3( self ):
		r = rendur.Create()
		r.assign("hello", "Hello")
		r.assign("world", "world")
		r.assign("my", "your")
		ret = r.display( r"examples/basic3" )
		self.assertEquals( ret, """Hello your world!
Hello world face
Hello big world""")

