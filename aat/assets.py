from flask_assets import Bundle

bundles = {
    'js': Bundle(
        'js/jquery-3.6.4.min.js',
        'bootstrap/js/popper.js',
        'bootstrap/js/bootstrap.js',
        'js/preview.js',
        'js/dropzones.js',
        'js/form-submit.js',
        'js/confirm.js',
        'dataTables/js/jquery.dataTables.min.js',
        'dataTables/js/dataTables.bootstrap5.min.js',
        'js/tables.js',
        'js/tooltips.js',
        'js/click-able-row.js',
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

    'table': Bundle(
        'dataTables/css/dataTables.bootstrap5.min.css',
        filters='cssmin',
        output='gen/table.%(version)s.css'
    ),

    'icons': Bundle(
        'fontawesome/css/all.min.css',
        'fontawesome/css/v4-shims.min.css',
        'fontawesome/css/brands.min.css',
        'fontawesome/css/solid.min.css',
        'fontawesome/css/regular.min.css',
        'fontawesome/css/fontawesome.min.css',
        filters='cssmin',
        output='gen/icons.%(version)s.css'
    ),

    'css': Bundle(
        'scss/main.scss', # Do not add CSS files here. See instuctions in the SCSS folder.
        filters='libsass',
        depends='scss/*.scss',
        output='gen/style.%(version)s.css'
    )
}
