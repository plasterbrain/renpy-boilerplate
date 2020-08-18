// Script to populate license text dynamically using URL parameters. :)
const urlParams = new URLSearchParams(window.location.search);
const params = urlParams.entries();

for(const param of params) {
	var textSlots = document.getElementsByClassName("param_" + param[0]);
	for(var textSlot of textSlots) {
		let value = param[1].replace("<", "&lt;");
		value = value.replace(">", "&gt;");
		textSlot.innerHTML = value;
	}
}

var copyrights = document.getElementsByClassName("param_copyrights");
if(copyrights.length) {
	var years = urlParams.get("years");
	var orgs = urlParams.get("orgs");
	years = years!=null ? urlParams.get("years").split(",") : [];
	orgs = orgs!=null ? urlParams.get("orgs").split(",") : [];

	var copytext = "";
	for(let i = 0; i < orgs.length; i++) {
		let year = i in years ? " " + years[i] : "";

		// Fix author emails/URLs in angular brackets
		let org = orgs[i].replace("<", "&lt;");
		org = org.replace(">", "&gt;");

		copytext += `Copyright (C)${year} ${org}<br/>`;
	}
	for(const textSlot of copyrights) {
		textSlot.innerHTML = copytext;
	}
}
