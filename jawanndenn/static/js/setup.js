/* Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
** Licensed under GNU GPL v3 or later
*/
var _REPLACEMENTS_IN_ORDER = [
    ['**', '<strong>', '</strong>'],
    ['*', '<em>', '</em>'],
    ['__', '<strong>', '</strong>'],
    ['_', '<em>', '</em>'],
    ['`', '<tt>', '</tt>'],
];

var _CLOSING_OF = {};
$.each( _REPLACEMENTS_IN_ORDER, function(_, row) {
    var prefix = row[0];
    var closing = row[2];

    _CLOSING_OF[prefix] = closing;
});

var exampleOptions = ['Apple', 'Banana', 'Orange', 'Papaya'];

var exampleVotesCache = {};

var createExampleVotes = function(options) {
    var examplePeople = ['Dmitri', 'Jule', 'Vered', 'Matthieu'];

    var exampleVotes = [];
    $.each( examplePeople, function( i, person ) {
        var votes = [];
        $.each( options, function() {
            votes.push( Math.random() > 0.5 );
        });
        exampleVotes.push( [person, votes] );
    });
    return exampleVotes;
};

var getExampleVotesCached = function(options) {
    if (options.length in exampleVotesCache) {
        return exampleVotesCache[options.length];
    } else {
        var exampleVotes = createExampleVotes(options);
        exampleVotesCache[options.length] = exampleVotes;
        return exampleVotes;
    }
};

var exampleConfigJson = JSON.stringify( {
        lifetime: "month",
        equal_width: false,
        title: 'Which fruit do _**you**_ like?',
        options: exampleOptions
        }, null, '  ' );

var resetConfig = function() {
    $('#config').val( exampleConfigJson );
};

var repairConfigLabel = function() {
    $('#config')[0].dispatchEvent(new Event('focus'))
}

// Excapes HTML and renders subset of markdown
var textToSafeHtml = function(text) {
    // KEEP IN SYNC with python server side!
    text = text
            .replace( /&/g, '&amp;' )
            .replace( /</g, '&lt;' )
            .replace( />/g, '&gt;' );

    var chunks = [];

    var opened = [];
    while (text.length) {
        var matched = false;

        $.each( _REPLACEMENTS_IN_ORDER, function(_, row) {
            var prefix = row[0];
            var opening = row[1];
            var closing = row[2];

            if ( text.startsWith(prefix) ) {
                if (opened.length && opened[opened.length - 1] == prefix) {
                    // Close tag
                    chunks.push( closing );
                    opened.pop();
                } else {
                    // Open tag
                    chunks.push( opening );
                    opened.push( prefix );
                }

                text = text.slice( prefix.length );

                matched = true;
                return false;
            }
        });

        if (! matched) {
            chunks.push( text[0] );
            text = text.slice(1);
        }
    }

    // Close all unclosed tags
    opened.reverse();
    $.each( opened, function(_, prefix) {
        chunks.push( _CLOSING_OF[prefix] );
    });

    return chunks.join('');
};

var processConfig = function(config) {
    return {
        equal_width: !!config.equal_width,
        title: textToSafeHtml( config.title ),
        options: $.map( config.options, textToSafeHtml )
    };
};

var prevConfigJson = '';
var prevWellformed = null;

var sync = function() {
    var configJson = $( '#config' ).val();

    var wellformed = true;
    var config = null;
    try {
        config = jQuery.parseJSON( configJson );
    } catch( err ) {
        wellformed = false;
    }

    if (wellformed != prevWellformed) {
        addRemoveGoodBad( $( "#config" ),
                'wellformed', 'malformed', wellformed );
        enableButton( $('#createButton'), wellformed );
        prevWellformed = wellformed;
    }

    if (wellformed) {
        var configJsonNormalized = JSON.stringify( config );
        if (configJsonNormalized != prevConfigJson) {
            prevConfigJson = configJsonNormalized;

            config = processConfig( config );

            var poll = $( "#poll" );
            poll.html( createPollHtml( config,
                    getExampleVotesCached( config.options ),
                    Mode.PREVIEW ) );

            if (config.equal_width) {
                equalizeWidth( poll );
            }
        }
    }
};

$( document ).ready(function() {
    resetConfig();
    repairConfigLabel();
    sync();
    setInterval( sync, 500 );
});
