redditFiller = function(subr, cont){
	var querypage = 1;
	var lastTime = new Date().getTime() / 1000;
	var showurl;

	var endswith = function (a, b) {
		return a.indexOf(b, a.length - b.length) !== -1;
	};

	var showInFrame = function (link) {
		return "<iframe width=800px height=600px src=" + link + "></iframe> <br />"
	};

	var onlyShowLink = function (link) {
		return '<br /><a href="' + link + '">' + link + '</a><br /><br />';
	};

	var modifyYoutubeLink = function (link) {
		return link.replace(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)/g, '<iframe width="800" height="540" src="http://www.youtube.com/embed/$1" frameborder="0" allowfullscreen></iframe>');
	};

	var showImage = function (link) {
		return '<a href="' + link + '"><img style="width:800px;height:inherit;" src="' + link + '"></img></a>';
	};


	var insertPosts = function (post){
	  if ((post.url.indexOf("youtube.com") !== -1) || (post.url.indexOf("youtu.be") !== -1)) {
	      showurl = modifyYoutubeLink(post.url);

	  } else if (post.url.indexOf("www.reddit.com") !== -1) {
	      showurl = onlyShowLink(post.url);

	  } else if (endswith(post.url, "/")) {
	      showurl = onlyShowLink(post.url);

	  } else if (post.url.indexOf("itunes.apple.com") !== -1) {
	      showurl = onlyShowLink(post.url);

	  } else if ((post.url.indexOf("imgur.com") !== -1) &&
				 !(endswith(post.url, ".jpg") ||
				  endswith(post.url, ".png") ||
				  endswith(post.url, ".gif")
				 )) {
	      showurl = showInFrame(post.url);

	  } else if (post.url.indexOf("deviantart.com") !== -1) {
	      showurl = showInFrame(post.url);

	  } else {
		  showurl = showImage(post.url);
	  };

	  data = [
	  "\n<br />",
	  "<h2>[" + post.subreddit + "]",
	  '<a href="' + post.linkToPage + '">' + post.title + '</a> (' + post.ncomments + ') </h2>',
	  showurl,
	  '<br /><hr />',
	  ].join('\n');

	  $("#" + cont).append(data);
	};

	var processJson = function(result) {
	  console.log('Hooray... got result from api call');
	  console.log(result);
	  result.map(insertPosts);
	};

	var loadContent = function(){
	  var apiurl = "/reddit/api/v1/get_posts?subr=" + subr + "&page=" + querypage + "&count=5";
	  console.log(apiurl);
	  $.getJSON(apiurl, processJson);
	  querypage = querypage + 1;
	};

	var nodeInScreen = function(node) {
	  var win = $(window);
	  var vbottom = win.scrollTop() + win.height();
	  var btop = node.offset().top;
	  console.log(btop, vbottom);
	  if (btop < vbottom) {
		  return true;
	  }
	  return false;
	};

	var onScroll = function(){
	  if (nodeInScreen($("#showmorediv"))) {
		var currentTime = new Date().getTime()/1000;
		console.log('showmore visible');
		if (currentTime - lastTime > 0.2) {
		  console.log("will load stuff");
		  loadContent();
		  lastTime = currentTime;
		} else {
		  console.log("too soon");
		}
	  };
	};

	$(window).scroll(onScroll);
	loadContent();
};