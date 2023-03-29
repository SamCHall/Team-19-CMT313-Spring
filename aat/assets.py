from flask_assets import Bundle

bundles = {
    'js': Bundle(
        'bootstrap/js/popper.js',
        'bootstrap/js/bootstrap.js',
        'js/script.js',
        'js/dropzones.js',
        'js/form-submit.js',
        'js/confirm.js',
        # 'js/example.js', <- Copy this format to add a file, making sure to include the comma at the end.
        filters='jsmin',
        output='gen/script.%(version)s.js'
    ),

    # JS used to graphs, only imported on pages with graphs
    'graph': Bundle(
        'js/plotly-2.18.2.min.js',
        'js/display-graph.js',
        filters='jsmin',
        output='gen/graph.%(version)s.js'
    ),

    'css': Bundle(
        'scss/main.scss', # Do not add CSS files here. See instuctions in the SCSS folder.
        filters='libsass',
        depends='scss/*.scss',
        output='gen/style.%(version)s.css'
    )
}
