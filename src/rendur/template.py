import re
import os

"""
Modifier
	Main class that defines the file template
"""
class Modifier(dict):
    def set(self, key):
        def setter(func):
            self[key] = func
            return func
        return setter

"""
Template
	Main class that defines the file template
"""
class Template(object):
	_templateName = ""
	_templateFilename = ""
	_templateFile = None
	_tagSimpleVarRe = None
	_tagComplex = None
	_openTag = r"{{"
	_closeTag = r"}}"
	_templateExt = ".tpl"
	_context = None

	def __init__( self, templateName ):
		super( Template, self ).__init__()
		self._templateFilename = templateName + self._templateExt
		self._templateName = os.path.basename( templateName )
		self._createTagRE()
		self._loadTemplateFile( self._templateFilename )

	def _loadTemplateFile( self, fileName ):
		f = open( fileName, "r" )
		try:
			self._templateFile = f.read()
		except IOError as e:
			print "Error reading template: %s" % fileName
		finally:
			f.close()

	def _createTagRE( self ):        
		tagspec = {
			'opentag': re.escape(self._openTag),
			'closetag': re.escape(self._closeTag)
		}

		tag = r"%(opentag)s?(.+?)\1?%(closetag)s+"
		self._tagSimpleVarRe = re.compile( tag % tagspec )

		tag = r"%(opentag)s?#(.+?) (.+?)\1?%(closetag)s+"
		self._tagComplex = re.compile( tag % tagspec )

	def render( self, context = None ):
		self._context = context
		self._parse( context )
		return self._templateFile

"""
RenderTemplate
	Class to render out a template
"""
class RenderTemplate( Template ):
	parsefunc = Modifier()
	def __init__( self, templateName ):
		super( RenderTemplate, self ).__init__( templateName )

	def _parseSimpleVars( self, context ):
		while True:
			match = self._tagSimpleVarRe.search( self._templateFile )
			if match is None:
				break
			var_tag = match.group(0)
			var_name = match.group(1)

			var_name = var_name.strip()
			var_tag = var_tag.strip()

			self._templateFile = self._templateFile.replace( var_tag, context[ var_name ] )

	def _parseComplex( self, context ):
		while True:
			match = self._tagComplex.search( self._templateFile )
			if match is None:
				break
			var_tag = match.group(0)
			function_name = match.group(1)
			params = match.group(2)

			params = params.strip()
			function_name = function_name.strip()
			var_tag = var_tag.strip()

			func = self.parsefunc[ function_name ]
			replacement = func( self, params, context )

			self._templateFile = self._templateFile.replace( var_tag, replacement )

	def _parse( self, context ):
		self._parseComplex( context )
		self._parseSimpleVars( context )

	@parsefunc.set( "include" )
	def _funcInclude( self, param, context ):
		t = RenderTemplate( param )
		return t.render( self._context )

"""
RenderTemplate
	Class to render out a template
"""
class CompileTemplate( Template ):
	parsefunc = Modifier()
	def __init__( self, templateName ):
		super( CompileTemplate, self ).__init__( templateName )

	def _compileTemplate( self ):
		js = []
		js.append( "var " + self._templateName + " = {};\n" )
		js.append( self._templateName + ".index = {\n" )
		js.append( "	render: function(args) {\n" )
		js.append( "		var t = [];\n" )

		for line in iter( self._templateFile.splitlines() ):
			self._compileLine( line, js )

		js.append( "		return t.join('');\n" )
		js.append( "	}\n" )
		js.append( "};" )
		return "".join( js )

	def _compileSimpleLine( self, line, ctx ):
		firstvar = True
		sufsufix = ""
		found = False
		while True:
			match = self._tagSimpleVarRe.search( line )
			if match is None:
				break
			found = True
			tag = match.group(0)
			var = match.group(1)

			tag = tag.strip()
			var = var.strip()

			prefix = ""
			preprefix = ""
			suffix = ""
			sufsufix = ""

			if line.find( tag ) > 0:
				prefix = "' + "
				preprefix = "'"

			if line.rfind( tag ) < ( len( line ) - len( tag ) ):
				suffix = " + '"
				sufsufix = "'"

			#if first var, add the preprefix
			if firstvar:
				line = preprefix + line
				firstvar = False

			line = line.replace( tag, prefix + "args." + var + suffix )
		
		firstquote = ""
		if not found:
			firstquote = "'"
		return "		t.push(" + firstquote + line + sufsufix + " + '\n');\n"

	def _compileFunction( self, line, ctx, foundFunction ):
		while True:
			match = self._tagComplex.search( line )
			if match is None:
				break
			foundFunction = True
			var_tag = match.group(0)
			function_name = match.group(1)
			params = match.group(2)

			params = params.strip()
			function_name = function_name.strip()
			var_tag = var_tag.strip()

			func = self.parsefunc[ function_name ]
			replacement = func( self, params, ctx )
			line = line.replace( var_tag, replacement )
		return line

	def _compileLine( self, line, ctx ):
		foundFunction = False
		cline = self._compileFunction( line, ctx, foundFunction )

		"""Cant have a function and simple vars on one line"""
		if not foundFunction:
			cline = self._compileSimpleLine( cline, ctx )
		
		ctx.append( cline )

	def _parse( self, context ):
		self._compileTemplate( )

	@parsefunc.set( "include" )
	def _compileFuncInclude( self, param, context ):
		name = os.path.basename( param )
		return name + ".index.render( args )"

