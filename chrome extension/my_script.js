document.addEventListener('keydown', function (key) {
	//If the space key is pressed
	if (key.keyCode == 32 || key.keyCode == 13) {
		var input_div = document.activeElement;
		if (input_div.tagName == "input" && input_div.className == "search-input" && input_div.id == "search-query" && input_div.name == "q"){
			alert(input_div.value);
			//send this hashtag to summarization api
		}
			
	}
});

