import re
import os
from template import *

"""
Rendur
	This is the main 'engine' class
"""
class Rendur:
	_bundler = None
	_templateVars = {}

	def __init__( self ):
		self._bundler = Bundler()

	def getBundler( self ):
		return self._bundler

	def assign( self, key, value ):
		self._templateVars[ key ] = value

	def display( self, templateFile ):
		tpl = RenderTemplate( templateFile )
		return tpl.render( self._templateVars )

	def compile( self, templateFile ):
		ctpl = CompileTemplate( templateFile )
		return ctpl.render()


"""
Bundler
	Bundles up client side javascript requirements and template compiles into a single file.
	The bundle is cached on the server so it only needs to be built when any of the input files change
"""
class Bundler:
	_requiredFileNames = []
	_appendContent = ""

	def require( self, jsFileName ):
		try:
			file = open( jsFileName, "r" );
			self._requiredFileNames.append( jsFileName )
		except IOError as e:
			print "Error opening %s" % ( jsFileName )

	def append( self, content ):
		self._appendContent = self._appendContent + content

	def makeBundle( self, filename ):
		if len( self._requiredFileNames ) == 0:
			return False
		
		for curFile in self._requiredFileNames:
			self.append( self.readInputFile( curFile ) )
			self.writeOutputFile( filename, fileContent )
		return True

		
	def writeOutputFile( self, filename, content ):
		try:
			f = open( filename, "w" )
			f.write( content )
			f.close()
		except IOError as e:
			print "Error writing output file: %s" % filename


	def readInputFile( self, filename ):
		ret = ""
		try:
			f = open( filename, "r" )
			ret = f.read()
			f.close()
		except IOError as e:
			print "Error opening input file: %s" % filename
		return ret
	

