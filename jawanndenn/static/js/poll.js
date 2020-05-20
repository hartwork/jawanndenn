/* Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
** Licensed under GNU GPL v3 or later
*/
var VOTED_YES_CLASS = 'votedYes';
var VOTED_NO_CLASS = 'votedNo';
var YET_TO_VOTE_CLASS = 'yetToVote';

var _UNICODE_HEAVY_CHECK_MARK = '\u2714';
var _UNICODE_HEAVY_BALLOT_X = '\u2718';

var Mode = {
    PREVIEW: true,
    LIVE: false,
};

// also used by setup.js
var addRemoveGoodBad = function(selector, goodClass, badClass, good) {
    if (good) {
        selector.addClass( goodClass );
        selector.removeClass( badClass );
    } else {
        selector.addClass( badClass );
        selector.removeClass( goodClass );
    }
};

var _addHeaderRow = function(table, options) {
    var tr = table.child( tag('tr') );
    tr.child( tag('td') );
    $.each( options, function( i, option ) {
        tr.child( tag('td', {
                class: 'optionLabel'
            }) ).child( option );
    });
    tr.child( tag('td') );
};

var _addExistingVoteRows = function(table, options, votes) {
    var votesPerOption = [];
    $.each( options, function( j, option ) {
        votesPerOption.push( 0 );
    });
    $.each( votes, function( i, personVotes ) {
        var person = personVotes[0];
        var votes = personVotes[1];

        var tr = table.child( tag('tr') );
        tr.child( tag('td', {
                    class: 'person',
                }) ).child( person );
        $.each( options, function( j, option ) {
            var tdClass = 'vote';
            if (votes[j]) {
                votesPerOption[j] = (votesPerOption[j] + 1);

                tdClass += ' ' + VOTED_YES_CLASS;
                var spanBody = _UNICODE_HEAVY_CHECK_MARK;
            } else {
                tdClass += ' ' + VOTED_NO_CLASS;
                var spanBody = _UNICODE_HEAVY_BALLOT_X;
            }
            tr.child( tag('td', {
                        class: tdClass,
                    }) )
                    .child( tag('span') )
                    .child( spanBody );
        });
        tr.child( tag('td') );
    });
    return votesPerOption;
};

var _addCurrentPersonRow = function(table, options, previewMode) {
    var tr = table.child( tag('tr') );
    var inputAttr = {
                id: 'voterName',
                name: 'voterName',
                type: 'text',
                class: 'person',
                placeholder: 'Your name'
            };
    if (! previewMode) {
        inputAttr.autofocus = 'autofocus';
        // NOTE: onchange fires "too late"
        inputAttr.onkeydown = 'onChangeVoterName(this);';
    }
    tr.child( tag('td', {
                class: 'person'
            }) ).child( tag('input', inputAttr) );

    $.each( options, function( j, option ) {
        var checkbox = tag('input', {
                    type: 'checkbox',
                    id: 'option' + j,
                    name: 'option' + j,
                    class: 'filled-in',
                    onclick: 'onClickCheckBox(this);'
                });
        var label = tag('label');
        label.child( checkbox );
        label.child( tag('span') );
        var td = tr.child( tag('td', {
                id: 'optionTd' + j,
                class: 'vote ' + YET_TO_VOTE_CLASS,
            }));
        td.child( label );
    });
    var toolsTd = tr.child( tag('td') );
    toolsTd.child( tag('input', {
                id: 'submitVote',
                type: 'submit',
                disabled: 'disabled',
                class: 'waves-effect waves-light btn',
                value: 'Save',
            }));
};

var _addSummaryRow = function(table, options, votesPerOption) {
    var tr = table.child( tag('tr') );
    tr.child( tag('td') );
    $.each( options, function( j, option ) {
        var tdAttr = {
                    class: 'vote',
                    id: 'sum' + j,
                };
        if (votesPerOption[j] > 0) {
            tdAttr.class += ' sumNonZero';
        }
        tr.child( tag('td', tdAttr) ).child( votesPerOption[j] );
    });
    tr.child( tag('td') );
};

var createPollHtml = function(config, votes, previewMode, csrf_token) {
    var div = tag('div', {
                class: 'card-panel'
            });
    div.child( tag('h2', {
                class: 'question'
            }) ).child( config.title );

    var form = div.child( tag('form', {
                id: 'pollForm',
                method: 'POST',
            }));
    form.child( tag('input', {
                type: 'hidden',
                name: 'csrfmiddlewaretoken',
                value: csrf_token,
            }));
    var table = form.child( tag('table', {
            id: 'pollTable'
            }) );

    _addHeaderRow(table, config.options);
    var votesPerOption = _addExistingVoteRows(table, config.options, votes);
    _addCurrentPersonRow(table, config.options, previewMode);
    _addSummaryRow(table, config.options, votesPerOption);

    return toHtml( div );
};

var enableButton = function(selector, enabled) {
    if (enabled) {
        selector.removeAttr('disabled');
    } else {
        selector.attr('disabled', 'disabled');
    }
};

var syncSaveButton = function() {
    var good = ($( '#voterName' ).val().trim().length > 0);
    var saveButton = $( '#submitVote' );
    enableButton(saveButton, good);
};

var onClickCheckBox = function(checkbox) {
    var diff = checkbox.checked ? +1 : -1;
    var sumTdId = checkbox.id.replace( /^option/, 'sum' );
    var sumTd = $( '#pollTable tr td#' + sumTdId );
    var oldSum = parseInt(sumTd.html());
    var newSum = oldSum + diff;

    sumTd.html( newSum );
    if ( oldSum === 0 || newSum === 0 ) {
        if ( newSum === 0 ) {
            sumTd.removeClass( 'sumNonZero' );
        } else {
            sumTd.addClass( 'sumNonZero' );
        }
    }

    var optionTdId = checkbox.id.replace( /^option/, 'optionTd' );
    var optionTd = $( '#pollTable tr td#' + optionTdId );
    optionTd.removeClass( YET_TO_VOTE_CLASS );
    addRemoveGoodBad( optionTd, VOTED_YES_CLASS, VOTED_NO_CLASS,
            checkbox.checked );
};

var onChangeVoterName = function(inputElem) {
    // Without delay we still get the old value
    // on access in Chromium.
    setTimeout( syncSaveButton, 1 );
};

var equalizeWidth = function(poll) {
    var optionLabels = $( 'td.optionLabel', poll );
    var optionLabelWidths = optionLabels.map( function() {
        return $(this).width();
    }).get();
    var maxLabelWidth = Math.max.apply(null, optionLabelWidths);
    optionLabels.each( function() {
        var jitter = Math.floor( Math.random() * 3 );
        $(this).width( maxLabelWidth + jitter );
    });
}
