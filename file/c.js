function get_text(el) {
    if (el == undefined) {
        return ""
    }
    if (el.innerText == undefined) {
        return el.textContent;
    } else {
        return el.innerText;
    }
}

uri = "http://groups.google.com/group/couchdb-relax/post"

title = get_text(document.getElementsByTagName('h1')[0])

uri += "?subject=" + escape("Comment on \"" + title + "\"")

// @@ add support for more types of element

// @@ do the split join to normalise whitespace

function add_comment_links() {
    var paras = document.getElementsByTagName('p');
    for (var i = 0; i < paras.length; i++) {
        var current = paras[i];
        if (!current || current.className != "") {
            continue;
        }
        var body = "From " + top.location.href + "\n\n> " + get_text(current)
        var current_uri = uri + "&body=" + escape(body);
        var comment_a = document.createElement('a');
        comment_a.href = current_uri;
        comment_a.className = "comment";
        comment_a.appendChild(document.createTextNode("点评或提问"));
        // get current's parent
        var text = current.firstChild;
        current.insertBefore(comment_a, text);
    }
}

window.onload = add_comment_links;
