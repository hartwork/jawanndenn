/* Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
** Licensed under GNU GPL v3 or later
*/
var exampleOptions = ['Apple', 'Banana', 'Orange', 'Papaya'];

var createExampleVotes = function(options) {
    var examplePeople = ['Joe', 'Lisa', 'Monica', 'Astrid'];

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

var exampleConfigJson = JSON.stringify( {
        title: 'Which fruit do *you* like?',
        options: exampleOptions
        }, null, '  ' );

var resetConfig = function() {
    $('#config').val( exampleConfigJson );
};

// Excapes HTML and renders subset of markdown
var textToSafeHtml = function(text) {
    // KEEP IN SYNC with python server side!
    return text
            .replace( /&/g, '&amp;' )
            .replace( /</g, '&lt;' )
            .replace( />/g, '&gt;' )
            .replace( /\*\*([^*]+)\*\*/g, '<strong>$1</strong>' )
            .replace( /\*([^*]+)\*/g, '<em>$1</em>' )
            .replace( /__([^_]+)__/g, '<strong>$1</strong>' )
            .replace( /_([^_]+)_/g, '<em>$1</em>' )
            .replace( /`([^`]+)`/g, '<tt>$1</tt>' )
            ;
};

var processConfig = function(config) {
    return {
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

            $( "#poll" ).html( createPollHtml( config,
                    createExampleVotes( config.options ),
                    Mode.PREVIEW ) );
        }
    }
};

$( document ).ready(function() {
    resetConfig();
    sync();
    setInterval( sync, 500 );
});
