/**
 * Pure JS Table of Contents
 * Copyright (c) 2020 Hendrik. All rights reserved.
 * https://codepen.io/aufmkolk/pen/RWKLzr
 *
 * This code is availble under the MIT License, which is copied below:
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.</p>
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
**/

document.addEventListener('DOMContentLoaded', function() {
	TableOfContents();
} );

function TableOfContents(container, output) {
	var toc = "";
	var level = 0;
	var container = document.querySelector(container) || document.querySelector('#main');
	var output = output || '#toc';

	container.innerHTML =
		container.innerHTML.replace(
			/<h([\d])>([^<]+)<\/h([\d])>/gi,
			function (str, openLevel, titleText, closeLevel) {
				if (openLevel != closeLevel) {
					return str;
				}

				if (openLevel > level) {
					toc += (new Array(openLevel - level + 1)).join('<ol>');
				} else if (openLevel < level) {
					toc += (new Array(level - openLevel + 1)).join('</li></ol>');
				} else {
					toc += (new Array(level+ 1)).join('</li>');
				}

				level = parseInt(openLevel);

				var anchor = titleText.replace(/ /g, "_");
				toc += '<li><a href="#' + anchor + '">' + titleText
					+ '</a>';

				return '<h' + openLevel + ' id="' + anchor + '">'
					+ titleText + '</h' + closeLevel + '>';
			}
		);

	if (level) {
		toc += (new Array(level + 1)).join('</ol>');
	}
	document.querySelector(output).innerHTML += toc;
};
