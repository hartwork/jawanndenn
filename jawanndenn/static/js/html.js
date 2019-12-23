/* Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
** Licensed under GNU GPL v3 or later
*/
var writeHtmlChunks = function(node, chunks) {
    if (node.hasOwnProperty('name')) {
        chunks.push( '<' + node.name );

        if (Object.keys(node.attr).length > 0) {
            $.each( node.attr, function( k, v ) {
                chunks.push( ' ' + k + '="' + v + '"' );
            });
        }

        chunks.push( '>' );

        $.each( node.children, function( i, v ) {
            writeHtmlChunks( v, chunks );
        });

        chunks.push( '</' + node.name + '>' );
    } else {
        chunks.push(node);
    }
};

var toHtml = function(node) {
    var chunks = [];
    writeHtmlChunks(node, chunks);
    return chunks.join('');
};

var tag = function(name, attr) {
    if (typeof attr === 'undefined') {
        attr = {};
    }

    return {
        name: name,
        attr: attr,
        children: [],

        child: function(node) {
            this.children.push(node);
            return node;
        },
    };
};
