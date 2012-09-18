var ABC = ABC ? ABC : {};
ABC.MEDIA = ABC.MEDIA ? ABC.MEDIA : {};
ABC.MEDIA.cinerama = function() {

	var _popUpUrl = cinerama_prefix + 'popup.htm?version=' + cinerama_version;
	var _playerURL = cinerama_prefix + 'cinerama.swf?version='
		+ cinerama_version;
	var _debugPlayerURL = cinerama_prefix + 'cinerama_debug.swf?version='
		+ cinerama_version;
	var _playlistVertical = cinerama_prefix + 'playlistVerticalWide.swf?version='
			+ cinerama_version;
	var _playlistHorizontal = cinerama_prefix
			+ 'playlistHorizontal.swf?version=' + cinerama_version;
	var _playlistVerticalSlimline = cinerama_prefix
			+ 'playlistVerticalSlimline.swf?version=' + cinerama_version;
	
	var _playlistURL = _playlistHorizontal;
	var _count = 0;
	var _embedObjectArray = [];
	this._embedObjects = new Object();
	
	var _wmode = "direct";
	
	var _deferPlayItemNumberObj = new Object();

	// PRIVATE functions
	
	var embed = function(embedObj) {
		var player = embedObj.debug == true?_debugPlayerURL:_playerURL;
		var params = {
			quality : "high",
			scale : "noscale",
			wmode : _wmode,
			allowscriptaccess : "always",
			allowfullscreen : true,
			bgcolor : embedObj.backgroundColour
		};

		var attributes = {
			id : embedObj.id
		};
		
		_embedObjectArray.push(embedObj);// for looping through objects.
		_embedObjects[embedObj.id] = embedObj;// for direct access to objects.
		
		swfobject.embedSWF(_playerURL, embedObj.id, embedObj.width,
				parseInt(embedObj.height) + parseInt(embedObj.controlHeight), "9.0.0", "expressInstall.swf",
				embedObj, params, attributes, onSuccess);
		
	}


	var onSuccess = function (e) {
		if (e.success) {
		
		}else{
			var src = unescape(_embedObjects[e.id].src);
	
			if(src.indexOf("rtmp") == -1 && src.indexOf(".mp4") > -1 && supportsVideo().mp4){
				var el = document.getElementById(e.id);
				var overlay = document.createElement('div');
				overlay.onclick = function (){insertHTML5Player(e)};
				overlay.style.position = "relative";
				var width = _embedObjects[e.id].width;
				var height = _embedObjects[e.id].height;
				
				var sp = '<span id="'+e.id+'-play-overlay" style="background: url('+cinerama_prefix+'images/overlay-play.png) no-repeat 50% 50%;display: block;position: absolute;height:'+height+'px;width:'+width+'px;"></span>';
				overlay.innerHTML += sp;
				el.parentNode.insertBefore(overlay, el.nextSibling);
				overlay.appendChild(el);
			}else{
				var error = document.createElement('p');
				error.innerHTML = "Flash version 9 or above required to view video: <a href='http://get.adobe.com/flashplayer/'>Get flash.</a>";
				error.className = "cinerama-embed-error";
				var el = document.getElementById(e.id);
				el.parentNode.insertBefore(error, el.nextSibling);
			}
		}
	}
	
	var insertHTML5Player = function (e){
		var src = unescape(_embedObjects[e.id].src);
		var image = _embedObjects[e.id].imageURL;
		var width = _embedObjects[e.id].width;
		var height = _embedObjects[e.id].height;
		var vid = document.createElement('p');
		var vidInsert = "<video id='"+e.id +"_video' autoplay controls width='"+width+"' height='"+height+"' poster="+image+">";
		vidInsert += 		"<source src='"+src+"' type='video/mp4'></source>"
		vidInsert += 	"</video>";
		vid.innerHTML = vidInsert;
		vid.className = e.id;
		var el = document.getElementById(e.id);
		var par = el.parentNode;
		par.insertBefore(vid, el.nextSibling);
		par.removeChild(el);
		var po = document.getElementById(e.id+'-play-overlay');
		po.style.display = "none";
		var vidElement = vid.firstChild;
		vidElement.addEventListener('canplay', function(evt) {this.play();}, false);
	}
	
	var supportsVideo = function () {
		var videoElement = document.createElement('video') || false;
		this.element = videoElement && typeof videoElement.canPlayType !== "undefined";
		this.mp4 = this.element && (videoElement.canPlayType("video/mp4") === "maybe" || videoElement.canPlayType("video/mp4") === "probably");
		this.ogg = this.element && (videoElement.canPlayType("video/ogg") === "maybe" || videoElement.canPlayType("video/ogg") === "probably");
		return this;
	};

	
	this.getSwfById = function (swfId) {
		if (navigator.appName.indexOf("Microsoft") != -1) {
			return window[swfId];
		} else {
			return document[swfId];
		}
	}

	var  getNewPlayerID = function() {
		return "player" + _count++;
	}

	var  getExtension = function (url) {
		if (url.length < 4)
			return null;
		var u = url.split("?")[0];
		var e = u.substr(u.length - 5);
		var s = e.split(".");
		if (s.length > 1) {
			return s[s.length - 1];
		} else {
			return null;
		}
	}

	var getSrcType = function (src) {
		var mrssExtensionsList = [ "xml", "htm", "html", "php", "asp" ];
		var ext = getExtension(src);
		for ( var i = 0; i < mrssExtensionsList.length; i++) {
			if (ext == mrssExtensionsList[i]) {
				return "mrss";
			}
		}

		var videoExtensionsList = [ "flv", "mp4" , "f4v", "m4v"];
		for ( var j = 0; j < videoExtensionsList.length; j++) {
			if (ext == videoExtensionsList[j]) {
				return "video";
			}
		}
		return null;
	}

	var trim = function(str) {
		return str.replace(/^\s*|\s*$/g, "");
	}
	
	var  getEmbedObj = function() {
		
		embedObj = new Object();
		embedObj.debug = cinerama.debug || false;;
		
		embedObj.id = getNewPlayerID();
		embedObj.src = "";
		embedObj.imageURL = "";
		embedObj.width = null;
		embedObj.height = null;
		embedObj.autoStart = false;
		embedObj.playlistType = cinerama.playlistType || "horizontal";
		embedObj.title = "";
		embedObj.srcType = "";
		embedObj.skin = cinerama.skin || "";
		embedObj.live = cinerama.live || false;
		embedObj.controlHeight = cinerama.controlHeight==null? 14 : cinerama.controlHeight;
		embedObj.controlFade = cinerama.controlFade == false?false:true;
		embedObj.controlY = cinerama.controlY != undefined ?cinerama.controlY: -53;
		embedObj.ratings = cinerama.ratings || false;
		embedObj.rateOnce = cinerama.rateOnce || false;
		embedObj.secure = cinerama.secure || false;
		embedObj.geoBlock = cinerama.geoBlock || false;
		embedObj.options = cinerama.options || false;
		embedObj.embedSrc = cinerama.embedSrc || false;
		embedObj.share = cinerama.share || false;
		embedObj.shareURL = escape(cinerama.shareURL || location.href);
		embedObj.supers = cinerama.supers || false;
		embedObj.scenePoints = cinerama.scenePoints || false;
		embedObj.pageURL = escape(location.href);
		embedObj.smooth = cinerama.smooth || false;
		embedObj.autoResize = cinerama.autoResize || false;
		embedObj.allowFullScreen = cinerama.allowFullScreen == false?false:true;
		embedObj.allowStageVideo = true;
		embedObj.keyboardControls = true;

		embedObj.textColour = cinerama.textColour || "#ffffff"; // white
		embedObj.highlightColour = cinerama.highlightColour || "#aaaaaa"; // grey
		embedObj.backgroundColour = cinerama.backgroundColour || "#000000";// black
		
		//playlist variables
		embedObj.autoAdvance = cinerama.autoAdvance == false?false:true;
		embedObj.playlistURL = cinerama.playlistURL || null;
		embedObj.playlistHeight = cinerama.playlistHeight || null;
		embedObj.playlistWidth = cinerama.playlistWidth  || null;

		_wmode = cinerama.wmode || _wmode;
		
		
		return embedObj;
	}
	
	var queryParamInterface = function(playerId){

		var id = swfobject.getQueryParamValue("pid")
		id = id == "" ? _embedObjectArray[0].id : id;
		
		if (playerId == id){
			
			var params = new Object();
			params.pid = swfobject.getQueryParamValue("pid");
			params.src = swfobject.getQueryParamValue("src");
			params.title = swfobject.getQueryParamValue("title");
			params.image = swfobject.getQueryParamValue("image");
			params.autostart = swfobject.getQueryParamValue("autostart");
			params.item = swfobject.getQueryParamValue("item");
			params.time = swfobject.getQueryParamValue("time");
			params.secure = swfobject.getQueryParamValue("secure");
			
			params.pid = params.pid == "" ? _embedObjectArray[0].id : params.pid;
			params.src = params.src == "" ? null : params.src;
			params.image = params.image == "" ? null : params.image;
			params.autostart = params.autostart == "" ? false : params.autostart == "true"?true:false;
			params.item = params.item == "" ? null : params.item;
			params.time = params.time == "" ? null : params.time;
			params.secure = params.secure == "" ? null : params.secure == "true"?true:false;
			
			if(params.secure != null){
				cinerama.setSecure(params.pid,params.secure);
			}
			
			if(params.item){
				cinerama.playItemNumber(params.pid,params.item);
			}

			if(params.src ){
				if(params.autostart){
					cinerama.playMedia(params.pid,params.src,params.title);
				}else{
					cinerama.loadMedia(params.pid,params.src,params.title);
				}
			}

			if(params.time){
				cinerama.seekVideo(params.pid,params.time);
			}
			

			if(params.src){
				return true;
			}else{
				return false;
			}
		}else{
			
			return false;
		}
	}
	
	var  testForImage = function(id,embedObj){
		if (document.getElementById(id).tagName == "IMG") {
			
			if (document.getElementById(id).src) {
				embedObj.imageURL = escape(document.getElementById(id).src);
			}
			
			if (embedObj.title == "") {
				embedObj.title = document.getElementById(id).alt;
			}
			
			if (embedObj.width == null) {
				embedObj.width = document.getElementById(id).width;
			}

			if (embedObj.height == null) {
				embedObj.height = document.getElementById(id).height;
			}
		}
	}
	
	
	// PUBLIC
	return {

		embedPlayer : function(id, src, width, height, title, autoStart) {
			var embedObj = getEmbedObj();
			embedObj.id = id;
			embedObj.src = escape(trim(src));
			embedObj.width = width || embedObj.width;
			embedObj.height = height || embedObj.height;
			embedObj.title = escape(title || embedObj.title);
			embedObj.autoStart = autoStart || embedObj.autoStart;

			embedObj.srcType = getSrcType(src) || this.srcType || "mrss";

			if (document.getElementById(id) == null) {
				swfobject.addDomLoadEvent(function() {
						testForImage(id,embedObj);
						embed(embedObj);
					});
			} else {
				testForImage(id,embedObj);
				embed(embedObj);
			}
		},

		playerReady : function(playerId) {
			this.onPlayerReady(playerId);
			return(queryParamInterface(playerId));
		},

		playMedia : function(playerId, src, title) {
			src = trim(src);	
			if (getSrcType(src) == "mrss") {
				this.playMRSS(playerId, src, title);
				return;
			}
			if (getSrcType(src) == "video") {
				this.playVideo(playerId, src, title);
				return;
			}
			
			this.playMRSS(playerId, src, title);
		},

		loadMedia : function(playerId, src, title) {
			src = trim(src);
			if (getSrcType(src) == "mrss") {
				this.loadMRSS(playerId, src, title);
				return;
			}

			if (getSrcType(src) == "video") {
				this.loadVideo(playerId, src, title);
				return;
			}
			this.loadMRSS(playerId, src, title);
		},
		

		playVideo : function(playerId, src, title) {
			if(src != _embedObjects[playerId].src){
				_embedObjects[playerId].src = src;
				getSwfById(playerId).playVideo(src, title);
				this.removePlaylist(playerId);
			}
		},

		loadVideo : function(playerId, src, title) {
			if(src != _embedObjects[playerId].src){
				_embedObjects[playerId].src = src;
				getSwfById(playerId).loadVideo(src, title);
				this.removePlaylist(playerId);
			}
		},

		playMRSS : function(playerId, src) {
			_embedObjects[playerId].src = src;
			try {
				getSwfById(playerId).playMRSS(src);
			} catch (e) {
			}
		},

		loadMRSS : function(playerId, src) {
			_embedObjects[playerId].src = src;
			try {
				getSwfById(playerId).loadMRSS(src);
			} catch (e) {
			}
		},
		
		pauseVideo : function(playerId) {
			getSwfById(playerId).pauseVideo();
		},
		
		seekVideo : function(playerId,seconds) {
			getSwfById(playerId).seekVideo(seconds);
		},

		playItemNumber : function(playerId, itemNumber) {
			
			var playlist = getSwfById("pl_" + playerId);
		
			if (playlist) {
				if (getSwfById(playerId).getSrcUrl() == getSwfById("pl_" + playerId).getSrcUrl()){
					playlist.playItemNumber(itemNumber);
				}else{
					playlist.setItemNumber(itemNumber);
				}
			} else {
				_deferPlayItemNumberObj["pl_" + playerId] = itemNumber;
			}
		},

		
		setSecure : function(playerId, bool) {
			this.secure = bool;
			try{
				if (getSwfById(playerId)) {
					getSwfById(playerId).secure(bool);
				}
			}catch(e){};
		},
		
		setLive : function(playerId, bool) {
			this.live = bool;
			if (getSwfById(playerId)) {
				getSwfById(playerId).live(bool);
			}
		},
		
		setAutoAdvance : function(playerId, bool) {
			_embedObjects[playerId].autoAdvance = bool;
			if (getSwfById(playerId)) {
				getSwfById("pl_" + playerId).setAutoAdvance(bool);
			}
		},

		popUpPlayer : function(playerId) {
			this.pauseVideo(playerId);
			var time = getSwfById(playerId).getTime();
			var src = getSwfById(playerId).getSrcUrl();
			var title = getSwfById(playerId).getTitle();
			var vidWidth = getSwfById(playerId).getStageWidth();
			var vidHeight = getSwfById(playerId).getStageHeight();
			var windowWidth = vidWidth;
			var windowHeight = vidHeight + 14
			var res = window.open(_popUpUrl+"&src="+src+"&time="+time+"&title="+title+"&vidWidth="+vidWidth+"&vidHeight="+vidHeight+"&autostart=true","popup","location=1,status=1,scrollbars=0,width="+windowWidth+",height="+windowHeight+""); 
			return false;
		},

		hideAllPlayers : function() {
			for ( var k = 0; k < _embedObjectArray.length; k++) {
				document.getElementById(_embedObjectArray[k].id).style.visibility = "hidden";
				if (document.getElementById("pl_" + _embedObjectArray[k].id)) {
					document.getElementById("pl_" + _embedObjectArray[k].id).style.visibility = "hidden";
				}
			}
		},

		showAllPlayers : function() {
			for ( var k = 0; k < _embedObjectArray.length; k++) {
				document.getElementById(_embedObjectArray[k].id).style.visibility = "visible";
				if (document.getElementById("pl_" + _embedObjectArray[k].id)) {
					document.getElementById("pl_" + _embedObjectArray[k].id).style.visibility = "visible";
				}
			}
		},
		
		closeConnection : function(playerId) {
			getSwfById(playerId).closeConnection();
		},
	
		// PRIVATE
		playlistItemClicked : function(playerId, src, title, index) {
			getSwfById(playerId).playVideo(src, title);
			this.onPlaylistItemClicked(playerId, src, title, index);
		},
		
		playListReady : function(playerId, playlistURL) {
			if(_deferPlayItemNumberObj[playerId]){
				getSwfById(playerId).playItemNumber(_deferPlayItemNumberObj[playerId]);
				_deferPlayItemNumberObj[playerId] = null;
			}
			this.onPlaylistReady(playerId, playlistURL);
		},
		
		streamComplete : function(playerId) {
			this.onStreamComplete(playerId);
			getSwfById("pl_" + playerId).streamComplete();
		},

		stateChange : function(playerId, state) {
			this.onStateChange(playerId,state);
			getSwfById("pl_" + playerId).onStateChange(state);
		},
		
		
		multiItemMRSS : function(playerId) {
			var playList = getSwfById("pl_" + playerId);
			var player = getSwfById(playerId);
			var width;
			
			if (playList == undefined || playList.parentNode == undefined) {
				var playlistDiv = document.createElement('div');
				playlistDiv.id = "pl_" + playerId;
				player.parentNode.insertBefore(playlistDiv, player.nextSibling);
			
				switch (_embedObjects[playerId].playlistType) {
				case "vertical":
					_playlistURL = _playlistVertical;
					width = 335;
					var height = player.getStageHeight();
					break;
				case "horizontal":
					_playlistURL = _playlistHorizontal;
					var br = document.createElement('br');
					player.parentNode.insertBefore(br, playlistDiv);
					width = player.getStageWidth();
					var height = 98;
					break;
				case "verticalSlim":
					_playlistURL = _playlistVerticalSlimline;
					width = 130;
					var height = player.getStageHeight();
					break;
				}
				
				// Override playlistURL, width and height if set;
				_playlistURL = _embedObjects[playerId].playlistURL || _playlistURL;
				width = _embedObjects[playerId].playlistWidth || width;
				height = _embedObjects[playerId].playlistHeight || height;
				//
				
				var params = {
					quality : "high",
					scale : "noscale",
					wmode : _wmode,
					allowscriptaccess : "always",
					allowfullscreen : true,
					bgcolor : this.backgroundColour
				};
				
				var flashvars = {
					id : "pl_" + playerId,
					autoStart : player.getAutoStart(),
					autoAdvance : _embedObjects[playerId].autoAdvance,
					itemNumber : 0,
					width : width,
					height : height,
					sourceURL : escape(player.getSrcUrl()),
					highlightColour : player.getHighlightColour(),
					textColour : player.getTextColour(),
					backgroundColour : player.getBackgroundColour()
				};
				
				var attributes = {};
				swfobject.embedSWF(_playlistURL, "pl_" + playerId, width,
						height, "9.0.0", "expressInstall.swf", flashvars,
						params, attributes);
			} else {
				playList.loadMRSS(player.getSrcUrl(), player.getAutoStart());
			}
			
			this.onMultiItemMRSS(playerId);
			
			
		},
		
		
		singleItemMRSS : function(playerId) {
			this.removePlaylist(playerId);
		},
		
		removePlaylist : function(playerId) {
			var playlistElement = document.getElementById( "pl_" +playerId);

			if(playlistElement){
				playlistElement.parentNode.removeChild(playlistElement);
				if(playlistElement.destroy){
					playlistElement.destroy();
				}
			}
		},
		
		nptToSeconds : function (nptTime){
			var seconds = 0;
			var timeArray = nptTime.split(":");
			switch(timeArray.length){
				case 1:
					seconds += parseInt(nptTime);
				break;
				case 2:
					seconds += parseInt(timeArray[1],10);
					seconds += parseInt(timeArray[0],10) * 60;
				break;
				case 3:
					seconds += parseInt(timeArray[2],10);
					seconds += parseInt(timeArray[1],10) * 60;
					seconds += parseInt(timeArray[0],10) * 3600;
				case 4:
					seconds += parseInt(timeArray[2],10);
					seconds += parseInt(timeArray[1],10) * 60;
					seconds += parseInt(timeArray[0],10) * 3600;
				break;
			}
			return seconds;
		},
		
		
		videoTime : function(time){
			
		},
		
		// CALLBACKS FROM PLAYER
		

		onPlayerReady : function(playerId){

		},
		
		onStreamComplete : function(playerId) {
			
		},
		
		unmetered : function(bool) {

		},
		
		/*
		 * States
		 * "PLAY_STATE","PAUSE_STATE","STOPPED_STATE","SEEKING_STATE","BUFFERING_STATE"
		 */
		onStateChange : function(playerId, state) {
			
		},
		
		onMultiItemMRSS : function(playerId) {
			
		},
		
		// CALLBACKS FROM PLAYLIST
		
		onChangeLink : function(playerId,linkURL, linkText) {
			
		},
		
		onPlaylistReady : function(playerId, playlistURL) {
			
		},
		
		onPlaylistItemClicked : function(playerId, src, title, index) {
			
		},
		
		trace : function(output) {
			alert(output);
		}

	}
}();

cinerama = ABC.MEDIA.cinerama;


