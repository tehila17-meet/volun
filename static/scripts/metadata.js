define(function(){
    return {
        pageGroups: [{"id":"ee16ea6d-3e90-bfa9-7906-e39bd2eed8fb","name":"Default group","pages":[{"id":"3d0c5e9d-d3a5-e9b0-b274-9a28693f708e","name":"Page 1"}]},{"id":"e35c0d62-333f-84cf-9850-578bd9dc6982","name":"Default group","pages":[{"id":"452c4959-3a62-ce5d-bc9d-ebaf39f6d61e","name":"Page 1"},{"id":"0407c007-e774-894a-32a6-62742cb728d2","name":"Page 2"},{"id":"2bee4bc1-2b7c-e316-7b11-d8f9caf7f781","name":"Page 3"},{"id":"9a039261-1532-6a4b-0601-63fb4e5ee98b","name":"Page 4"},{"id":"0fd5b2b6-10a6-10c5-d46d-b05d2b3729ef","name":"Page 5"},{"id":"e7b88dec-bee0-187f-7efe-5f00b80f6e0b","name":"Page 6"}]}],
        downloadLink: "//services.ninjamock.com/html/htmlExport/download?shareCode=V1RFK&projectName=Volunpeer",
        startupPageId: 0,

        forEachPage: function(func, thisArg){
        	for (var i = 0, l = this.pageGroups.length; i < l; ++i){
                var group = this.pageGroups[i];
                for (var j = 0, k = group.pages.length; j < k; ++j){
                    var page = group.pages[j];
                    if (func.call(thisArg, page) === false){
                    	return;
                    }
                }
            }
        },
        findPageById: function(pageId){
        	var result;
        	this.forEachPage(function(page){
        		if (page.id === pageId){
        			result = page;
        			return false;
        		}
        	});
        	return result;
        }
    }
});
