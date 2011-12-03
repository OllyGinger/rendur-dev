import unittest
import rendur

class TestBasicCompiles(unittest.TestCase):
	def test_basic_compile( self ):
		r = rendur.Create()
		ret = r.compile( r"examples/basic" )
		self.assertEquals( ret, """var basic = {};
basic.index = {
	render: function(args) {
		var t = [];
		t.push('Hello ' + args.planet + '!' + '\n');
		return t.join('');
	}
};""")

	def test_prefix_suffix( self ):
		r = rendur.Create()
		ret = r.compile( r"examples/basic2" )
		self.assertEquals( ret, """var basic2 = {};
basic2.index = {
	render: function(args) {
		var t = [];
		t.push(args.hello + ' world!' + '\n');
		t.push('Hello ' + args.world + '\n');
		t.push('I have no tags :(' + '\n');
		return t.join('');
	}
};""")

	def test_complex_prefix_suffix( self ):
		r = rendur.Create()
		ret = r.compile( r"examples/basic3" )
		self.assertEquals( ret, """var basic3 = {};
basic3.index = {
	render: function(args) {
		var t = [];
		t.push(args.hello + ' ' + args.my + ' world!' + '\n');
		t.push('Hello ' + args.world + ' face' + '\n');
		t.push(args.hello + ' big ' + args.world + '\n');
		return t.join('');
	}
};""")

	def test_function_include( self ):
		r = rendur.Create()
		ret = r.compile( r"examples/include1" )
		self.assertEquals( ret, "")
