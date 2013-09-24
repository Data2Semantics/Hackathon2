$(function() {
    $('#filebreadcrumb').hide();
    $('#progress').hide();

    $('#reposbreadcrumb').on('click', function(e) {
        $('#repositories').show();
        $('#actions').hide();
        $('#reposbreadcrumb').toggleClass('active');
        $('#filebreadcrumb').toggleClass('active');
        $('#filebreadcrumb').hide();
        $('#browse').hide();
    });

    $('.repository').on('click', function(e) {
        var clone_url = $(this).attr('clone_url');
        var name = $(this).attr('name');

        $('#repositories').hide();
        show_progress_bar('Initializing dataset ' + name);

        $.get('{{ url_for("github_clone") }}', {
            clone_url: clone_url,
            name: name
        }, function(data) {
            var name = data.name;
            var path = data.name;

            hide_progress_bar();

            $('#reposbreadcrumb').toggleClass('active');
            $('#filebreadcrumb').toggleClass('active');
            $('#filebreadcrumb').show();

            browse('#browse', '#actions', path, name);

            console.log("Showing #browse");
            $('#browse').show();

            console.log("Now showed #browse for the first time");

        });
    });
});

function show_progress_bar(message) {
    $('#progress_heading').text(message);
    $('#progress_message').text(message);
    $('#progress').show();
}

function hide_progress_bar() {
    $('#progress').hide();
}

function browse(browsepane, actionpane, path, name) {
    // Hide the actions
    $(actionpane).hide();


    // Retrieve JSON list of files
    $.get('{{ url_for("browse") }}', {
        path: path,
        name: name
    }, function(data) {
        var parent = data.parent;
        var files = data.files;

        // Clear the DIV containing the file browser.
        $(browsepane).empty();


        var heading = $('<h4></h4>');

        if (path.length < 50) {
            heading.append(path);
        } else {
            heading.append(path.substring(0, 10) + '...' + path.substring(path.length - 40));
        }


        $(browsepane).append(heading);


        var list = $('<div></div>');
        list.toggleClass('list-group');

        if (parent != '') {
            var up = $('<a class="list-group-item"><span class="glyphicon glyphicon-folder-open"></span><span style="padding-left: 1em;">..</span></a>');
            up.on("click", function(e) {
                browse(browsepane, actionpane, parent, name);
            });

            $(list).append(up);
        }



        $.each(files, function(index, value) {
            console.log(value);

            var a = $('<a></a>');

            a.toggleClass('list-group-item');

            if (value.type == 'dir') {
                var icon = $('<span class="glyphicon glyphicon-folder-open"></span>');
                a.append(icon);
                a.append('<span style="padding-left: 1em;">' + value.name + '</span>');
                a.on('click', function(e) {
                    browse(browsepane, actionpane, value.path, name);
                });
            } else {
                var icon = $('<span class="glyphicon glyphicon-file"></span>');
                a.append(icon);
                a.append('<span style="padding-left: 1em;">' + value.name + '</span>');

                var badge = $('<span></span>');
                badge.append(" (" + value.mimetype + ")");
                badge.toggleClass('badge');
                a.append(badge);

                a.on('click', function(e) {
                    $.get('{{ url_for("actions") }}', {
                        dataset: name,
                        name: value.name,
                        path: value.path,
                        type: value.type,
                        mimetype: value.mimetype
                    }, function(data) {
                        $(actionpane).html(data);
                        $(actionpane).show();
                    });
                });
            }


            list.append(a);
        });


        $(browsepane).append(list);
    });


}
