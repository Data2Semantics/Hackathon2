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
                        render_workflows(actionpane, data);
                        $(actionpane).show();
                    });
                });
            }


            list.append(a);
        });


        $(browsepane).append(list);
    });
}

function render_workflows(paneid, data){
    
    var pane = $(paneid);
    pane.empty();
    pane.append("<h4>Possible Actions for '"+data.name+"'");
    
    console.log(data);
    
    for (w in data.workflows) {
        
        var workflow = data.workflows[w];
        
        console.log("Now configuring "+workflow.id);
        console.log(workflow);
        
        var widget = $('<div></div>');
        widget.addClass('well');
        
        var workflow_heading = $('<p><strong>'+workflow.name+'</strong></p>');
        
        var workflow_description = $('<p>'+workflow.description+'</p>');
        
        // The "Run" Button
        var run_button = $('<a></a>');
        run_button.addClass('btn');
        run_button.addClass('btn-primary');
        run_button.attr('workflow',workflow.id);
        run_button.attr('filename',workflow.name);
        run_button.attr('dataset',data.dataset);
        run_button.attr('filepath',data.path);
        
        run_button.html('Run');
        
        run_button.on('click',function(){
            var button = $(this);
            console.log('Clicked '+button.attr('workflow'));
            
            button.removeClass('btn-primary');
            button.addClass('btn-info');
            button.addClass('disabled');
            
            button.html('Calling ...');
            
            $.get('{{ url_for("run_workflow") }}',
                  {filepath: button.attr('filepath'), workflow_id: button.attr('workflow'), filename: button.attr('filename'), dataset: button.attr('dataset')},
                  function(data){
                    var button = $('a[workflow="'+data.workflow_id+'"]');
                    
                    console.log('Running '+data.workflow_id);
                    button.html('Initializing...');
                    
                    check_status(data.workflow_id, data.source, true);
            });
        });
        
        widget.append(workflow_heading);
        widget.append(workflow_description);
        widget.append(run_button);
        
        pane.append(widget);
    }    
}

function check_status(workflow_id, filepath, continue_polling) {
    console.log("Checking status of "+workflow_id);
    $.get('{{ url_for("get_workflow_status") }}', {workflow_id: workflow_id, filepath: filepath}, function(data){
        
        var button = $('a[workflow="'+ data.workflow_id + '"]');
        
        console.log("Retrieved status "+data.status+" for "+data.workflow_id);
        if (data.status == 'finished') {
            button.removeClass('btn-info');
            button.addClass('btn-success');
            button.html('Done');
            
            show_report(workflow_id, filepath);
            
        } else if (data.status == 'error') {
            button.removeClass('btn-info');
            button.addClass('btn-danger');
            button.html('Error');
            
            $.get('{{ url_for("get_workflow_log") }}', {workflow_id: workflow_id, source: filepath}, function(data){
                if (data.result) {
                    var log_button = $('<a></a>');
                    log_button.addClass('btn');
                    log_button.addClass('btn-info');
                    log_button.html('Show Log');
                    log_button.attr('text',data.result);
                    
                    log_button.on('click', function(){
                        window.alert($(this).attr('text'));
                    
                    });
                }
                
            });

            
            
            
        } else if (data.status == 'running') {
            // Poll again in 10 seconds
            button.addClass('btn-info');
            button.html('Running...');
            console.log("Waiting 5 seconds...");
            setTimeout(function(){
                check_status(workflow_id, filepath, true)}, 5000);
        } else if (data.status == 'initializing') {
            // Poll again in 10 seconds
            button.addClass('btn-info');
            button.html('Initializing...');
            if (continue_polling) {
                console.log("Waiting 5 seconds...");
                setTimeout(function(){
                    check_status(workflow_id, filepath, true)}, 5000);
            }
        }
    }); 
}

function show_report(workflow_id, source) {
    $.get('{{ url_for("get_workflow_report") }}', {workflow_id: workflow_id, source: source}, function(data){
        var div = $("<div></div>");
        div.addClass('col-md-6');
        
        div.append(data);
        
        $("#report_widgets").append(div);
    });
}
