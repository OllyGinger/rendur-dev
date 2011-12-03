import cherrypy
import rendur


class MyWebsite( object ):
	def indexPage( self ):
		r = rendur.Create()
		r.assign( "title", "My Website title" )
		r.assign( "name", "Gaben" )
		return r.display( r"templates/index.tpl" )

	def pageTwo( self ):
		pass


class RunRendur( object ):
	def index( self ):
		web = MyWebsite()
		return web.indexPage()
	index.exposed = True



cherrypy.quickstart( RunRendur() )

