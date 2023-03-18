from flask_assets import Bundle

bundles = {
    'js': Bundle(
        'js/script.js',
        'js/dropzones.js',
        # 'js/example.js', <- Copy this format to add a file, making sure to include the comma at the end.
        filters='jsmin',
        output='gen/script.%(version)s.js'
    ),

    'css': Bundle(
        'scss/main.scss', # Do not add CSS files here. See instuctions in the SCSS folder.
        filters='libsass',
        depends='scss/*.scss',
        output='gen/style.%(version)s.css'
    )
}
