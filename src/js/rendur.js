$(document).ready(function() {
    $('#page2Link').click(function() {
		loadPage( "page2" );
	});
	$('#page1Link').click(function() {
		loadPage( "page1" );
	});
	$('#page3Link').click(function() {
		loadPage( "page3" );
	});
});

function loadPage( pageToLoad ) {
	$.ajax({
		url: "data.php?page=" + pageToLoad,
		success: Rendur.Renderer.postAjax,
		headers: { "X-ClientSideLoad": 1 }
	});
}



var Rendur = {};
Rendur.Renderer = { 
	registeredTemplates: {},

	addTemplate: function( templateName ) {
		var c = eval( templateName );
		registeredTemplates.push( { templateName: c } );
	},

	importTemplate: function( templateName, args ) {
		var _component = templateName.split( "." )[0];
		var _template = templateName.replace(_component + ".", "").replace(".", "_");
		var _render;
		try {
			_render = eval( _component + "." + _template + ".render" );	
		} catch( e ) {};
		if( _render ) {
			return _render( args );
		} else {
			return "";
		}
	},

	getTemplate: function( templateName ) {
		var _component = templateName.split( "." )[0];
		var _template = templateName.replace(_component + ".", "").replace(".", "_");
		var _tpl;
		try {
			_tpl = eval( _component + "." + _template  );	
		} catch( e ) {};
		if( _tpl ) {
			return _tpl;
		} else {
			return null;
		}
	},

	postAjax: function( data ) {
		var json = null;
		if (data.substr(0, 1) == "{" && data.substr(data.length - 1) == "}") {
		    try {
		        json = Rendur.parseJson(data);
		    } catch (e) {}
		}

		Rendur.Renderer.renderPage( json );
		
		if( typeof( json.url ) != "undefined" && typeof( json.pageTitle ) != "undefined" ) {
			Rendur.AjaxNavigation.addPageHistory( json, json.pageTitle, json.url );
		}
	},

	renderPage: function( jsonData ) {
		if( jsonData && typeof( jsonData.template ) != "undefined" ) {
			var html = Rendur.Renderer.getTemplate( jsonData.template ).render( jsonData.context );
			$("#content").html( html );
		}
	}
};
Rendur.parseJson = function(jsonstr) {
	return $.parseJSON(jsonstr);	
};

window.onpopstate = function( obj ) {
	Rendur.AjaxNavigation.onPopState( obj );
}
Rendur.AjaxNavigation = {
	canUseHTML5History: function() {
		return typeof( history ) != "undefined" && typeof( history.pushState ) != "undefined";
	},

	addPageHistory: function( data, title, url ) { 
		if( Rendur.AjaxNavigation.canUseHTML5History ) {
			history.pushState( data, title, url );
		}
	},

	onPopState: function( obj ) {
		Rendur.Renderer.renderPage( obj.state );
	}
};



var page1 = {};
page1.index =  {
	render: function( args ) {
		var c = [];
		c.push( '<!DOCTYPE html>\n' );
		c.push( '<html>\n' );
		c.push( '<head>\n' );
		c.push( '<script src="http://code.jquery.com/jquery-1.7.min.js" type="text/javascript"></script>\n' );
		c.push( '</head>\n' );
		c.push( '<body>\n' );
		c.push( '<h1>' + args.page_header + '</h1>\n' );
		c.push( '<button id="page2Link">Page 2</button>\n' );
		c.push( '<button id="page3Link">Page 3</button>\n' );
		c.push( '<script src="js/rendur.js" type="text/javascript"></script> \n' );
		c.push( '</body>\n' );
		c.push( '</html>\n' );
		return c.join("");
	}
};

var page2 = {};
page2.index =  {
	render: function( args ) {
		var c = [];
		c.push( '<!DOCTYPE html>\n' );
		c.push( '<html>\n' );
		c.push( '<head>\n' );
		c.push( '<script src="http://code.jquery.com/jquery-1.7.min.js" type="text/javascript"></script>\n' );
		c.push( '</head>\n' );
		c.push( '<body>\n' );
		c.push( '<h1>' + args.page_header + '</h1>\n' );
		c.push( '<button id="page1Link">Page 1</button>\n' );
		c.push( '<button id="page3Link">Page 3</button>\n' );
		c.push( '<script src="js/rendur.js" type="text/javascript"></script> \n' );
		c.push( '</body>\n' );
		c.push( '</html>\n' );
		return c.join("");
	}
};

var page3 = {};
page3.index =  {
	render: function( args ) {
		var c = [];
		c.push( '<!DOCTYPE html>\n' );
		c.push( '<html>\n' );
		c.push( '<head>\n' );
		c.push( '<script src="http://code.jquery.com/jquery-1.7.min.js" type="text/javascript"></script>\n' );
		c.push( '</head>\n' );
		c.push( '<body>\n' );
		c.push( '<h1>' + args.page_header + '</h1>\n' );
		c.push( '<button id="page1Link">Page 1</button>\n' );
		c.push( '<button id="page2Link">Page 2</button>\n' );
		c.push( '<script src="js/rendur.js" type="text/javascript"></script> \n' );
		c.push( '</body>\n' );
		c.push( '</html>\n' );
		return c.join("");
	}
};
