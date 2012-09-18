var ABC = ABC ? ABC : {};

ABC.SCIENCE = function () {

	var flashVideoPlayer
		= "http://www.abc.net.au/science/js/abcNews/flvplayer.swf";
	var flashAudioPlayer
		= "http://www.abc.net.au/science/js/abcNews/mp3player.swf";
	var inlineHolderImage
		= "http://www.abc.net.au/science/audio/img/audioPlayer.250.30.png";
	var inlineHolderImageWidth
		= 250;
	var inlineHolderImageHeight
		= 30;
	var inlineHolderImageAlt
		= "Click to play this audio";
	var inlineAudioImage
		= "<img src=\"" + inlineHolderImage
			+"\" width=\"" + inlineHolderImageWidth
			+"\" height=\"" + inlineHolderImageHeight
			+ "\" alt=\"" + inlineHolderImageAlt + "\" />";
	var selectedAudioId = "";
	
	jQuery(document).ready(function() {
	/*
	 $(this).next('div').slideToggle(200, 'linear')
   .siblings('div:visible').slideUp(200, 'linear');
	*/
		jQuery('li.navlink:not(.selected)').hover(
			function() {
				jQuery('ul', this).css('display', 'block');
				jQuery(this).addClass('hover');
			},
			function() {
				jQuery('ul', this).css('display', 'none');
				jQuery(this).removeClass('hover');
			}
		);
		
		jQuery("div.accordion div.item1").removeClass('item1');
		jQuery("div.accordion div.content").show();
		
		jQuery("div.accordion").accordion({
			header: "div.title",
			autoHeight: false
		});
		
		jQuery(this).prepareInlineAudio(inlineAudioImage);
		
		// Create Audio Page players
		 jQuery('div.audioPageAudio').createAudioPagePlayer();
		
		jQuery('div.inline div.player').click(function() {
			jQuery(this).playMedia();
		});
		
		jQuery('div.accordion div.content').click(function() {
			jQuery(this).playMedia();
		});
			
		jQuery('.goList').change(function() {
			var redirect = jQuery(this).find('option:selected').attr('value');
			location.href = redirect;
		});
		
		//	Refresh the img#karlCam every 10 seconds 
	
		var karlCam = setInterval(
			"jQuery('#karlCam').attr('src','/science/k2/stn/test.jpg?t=' + new Date().getTime())", 10000
			);
		
		//Return a NASA twitter feed
		
		jQuery("#nasaTwitter").searchTwitter(
			"http://search.twitter.com/search.json?q=+from%3AAP11_SPACECRAFT+OR+from%3AAP11_CAPCOM+OR+from%3Aap11_eagle&callback=?"
		);
		
				
	});
	/* jQuery specific funtions defined below */
	jQuery.fn.playMedia = function () {
	
		jQuery('div.inline div.player').each(function() {
			jQuery(this).clearPlayers();
		});
		
		jQuery('div.accordion div.content').each(function() {
			jQuery(this).clearPlayers();
		});
		
		if (jQuery(this).hasClass('video')) {
			jQuery(this).append(
				ABC.SCIENCE.attachMedia(
					jQuery(this).find('div.media').attr('id'),
					jQuery(this).find('a').attr('name'),
					'video',
					285,
					190,
					8,
					"#000000",
					true,
					flashVideoPlayer
				)
			);
		}
		
		if (jQuery(this).hasClass('audio')) {
			jQuery(this).append(
				ABC.SCIENCE.attachMedia(
					jQuery(this).find('div.media').attr('id'),
					jQuery(this).find('a').attr('name'),
					'audio',
					250,
					38,
					8,
					"#E4E4E4",
					true,
					flashAudioPlayer
				)
			);
		}
		
		jQuery(this).find('a.link').hide();
	
	}

	jQuery.fn.clearPlayers = function() {
	
		if (jQuery(this).find('object')) {
			jQuery(this).find('a.link').show();
			jQuery(this).find('object')
				.replaceWith(
					'<div class="media" id="'
					+ jQuery(this).find('object').attr("id")
					+ '"></div>'
				);
			ABC.SCIENCE.removeMedia(jQuery(this).find('object').attr("id"));
		}

	};
	
	jQuery.fn.prepareInlineAudio
		= function(_inlineAudioImage) {
		i = 0;
		jQuery('div.inline')
			.each(
				function() {
					i++;
					if (jQuery(this).hasClass('audio')) {
						audioFile
							= jQuery(this)
								.find('div.links a.mp3')
								.attr('href');
						jQuery(this).append(
							"<div class=\"player audio\">"
							+"<a class=\"link\" name=\""+audioFile+"\">"
							+_inlineAudioImage
							+"</a>"
							+"<div class=\"media\" id=\"inline_audio_"+i+"\">"
							+"</div>"
							+"</div>"
						);
					}
				});
	/* jQuery specific funtions defined above */
	};
	
		jQuery.fn.createAudioPagePlayer = function() {
			i = 0;
			return this.each(function() {
				//Give each element a unique ID
				i++;
				jQuery(this).find('.player').attr('id','audio_'+i);
				
				//For each link to an audio file
				jQuery(this).find('a.mp3').click(function(e) {
				
					//Stop the link action from occurring
					e.preventDefault();
									
					//Identify the parent container and the id and class of the player container 
					var audioSegment = jQuery(this).parent().parent();
					var playerID = jQuery(audioSegment).find('.player').attr('id');
					var playerClass = jQuery(audioSegment).find('.player').attr('class');
					
					if (playerID != undefined) {
						
						if (selectedAudioId != "") {
							jQuery("#"+selectedAudioId).before("<div id='"+selectedAudioId+"' class='player audio'></div>").remove(); 
						}
						
						//Deselect any existing selected audio blocks, and hide the comment
						jQuery('.audioPageAudio').each(function() {
							jQuery(this).removeClass('selectedAudio');
							jQuery(this).find('span.audioComment').css({'display':'none'});
						});
						
						//Add the active state class
						jQuery(audioSegment).addClass('selectedAudio');
						
						// show the blurb, and post-format it
						jQuery(audioSegment).find('span.audioComment').css({'display':'block'});
					
						// saving new ID for later... 
						selectedAudioId = playerID;
						
						//Attach the audio file player
						addAudio(
								playerID,
								jQuery(this).attr('href'),
								'audio',
								250,
								38,
								8,
								"#FFFFFF",
								true,
								flashAudioPlayer
						);
					}
				});
			});
		};
	
	//Get a Twitter search result in JSON and mark it up
	jQuery.fn.searchTwitter = function(url) {
		return this.each(function() {
			var myElement = jQuery(this);
			jQuery.getJSON(url, function(data){
				jQuery.each(data.results, function(i, item) {
					var itemLine =
						'<p style="clear: both; height: 55px;"><a href="http://www.twitter.com/'
						+ item.from_user + '"><img src="' + item.profile_image_url + '" style="width: 48px; height: 48px; float: left; margin-right: 1em;"> ' + item.from_user + '</a> - '
						+ item.text + '</p>';
					jQuery(myElement).append(itemLine);
				});
			});
			
			jQuery(this).ajaxError(function(event, request, settings){
				jQuery(myElement).append(
					//"<p>Error requesting page " + settings.url + "</p>");
					"<p>An error occurred, sorry</p>");
			});
			
		});
	};
	
	return {
	/* ABC.SCIENCE specific funtions defined below */
		attachMedia : function (
			_id, _url, _mediaType, _width, _height, _minVersion,
			_bgColor, _autoPlay, _videoPlayer) {
			
			if (_mediaType == 'audio') {
				mediaVars = "mediaURL="
					+_url
					+"&autoplay="
					+_autoPlay
					+"&glassyplayer=false&playershadow=false"
					+"&playerbgcolor=#cccccc&pausecolor=#ffffff"
					+"&scrubcolor=#ffffff&scrubbgcolor=#999999"
					+"&itemtimecolor=#000000&volumeiconcolor=#ffffff"
					+"&timetextcolor=#000000&loadingbarcolor=#666666"
					+"&loadingbgcolor=#000000";
			} else {
				mediaVars = 'mediaURL='+_url;
			}
			
			var att = {
						'data':_videoPlayer,
						'class':_mediaType,
						'width':_width,
						'height':_height,
						'align':'center'
						};
						
			var par = {
						'menu':'false',
						'flashvars':mediaVars,
						'bgcolor':_bgColor,
						'play':_autoPlay,
						'allowFullScreen':true
						};
						
			var id = _id;
			
			swfobject.createSWF(att, par, id);

		},
		
		removeMedia : function (_id) {
			swfobject.removeSWF(_id);
		}
		
	/* ABC.SCIENCE specific funtions defined above */
		
	}

}();

/* Pop-up function for ABC Local radio player */

function show_popup(url, width, height) {
	if (width == "") {width = 650};
	if (height == "") {height = 300};
//	popWin = window.open(url + "?width=" + width, "", "resizable=yes,toolbar=no,menubar=no,width=" + width + ", height=" + height + " ");
	popWin = window.open(url, "", "resizable=yes,toolbar=no,menubar=no,width=" + width + ", height=" + height + " ");
	popWin.focus();
}
function addAudio (_id, _url, _mediaType, _width, _height, _minVersion,_bgColor, _autoPlay, _videoPlayer) 
{
 	mediaVars = "mediaURL="
	+_url
	+"&autoplay="
	+_autoPlay
	+"&glassyplayer=false&playershadow=false"
	+"&playerbgcolor=#cccccc&pausecolor=#ffffff"
	+"&scrubcolor=#ffffff&scrubbgcolor=#999999"
	+"&itemtimecolor=#000000&volumeiconcolor=#ffffff"
	+"&timetextcolor=#000000&loadingbarcolor=#666666"
	+"&loadingbgcolor=#000000";
	var att = {
		'data':_videoPlayer,
		'class':_mediaType,
		'width':_width,
		'height':_height,
		'align':'center'
	};
	var par = {
		'menu':'false',
		'flashvars':mediaVars,
		'bgcolor':_bgColor,
		'play':_autoPlay,
		'allowFullScreen':true
	};
	var id = _id;
	swfobject.createSWF(att, par, id);
}
