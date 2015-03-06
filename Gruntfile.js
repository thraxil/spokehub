module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {                            // Task
      dist: {                            // Target
        options: {                    // Target options
          style: 'compressed'
        },
        files: {                                    // Dictionary of files
          'media/css/spokehub.css': 'media/sass/spokehub.scss',        // 'destination': 'source'
        }
      }
    },

    watch: {
      css: {
        files: [
          '**/*.sass',
          '**/*.scss'
        ],
        tasks: [
          'sass',
          'autoprefixer',
          'jshint'
        ]
      }
    },

    compass: {
      dist: {
        options: {
          sassDir: 'media/sass',
          cssDir: 'media/css',
          outputStyle: 'compressed'
        }
      }
    },

    jshint: {
      all: [
        'Gruntfile.js',
        'media/scripts/{,*/}*.js'
      ]
    },

    autoprefixer: {
      options: {
        browsers: ['> 1%', 'last 2 versions', 'Firefox ESR', 'Opera 12.1']
      },
      single_file: {
        src: 'media/css/spokehub.css',
        dest: 'media/css/main.css'
      }
    },

    concat: {
      dist: {
        src: [
          'media/components/jquery/dist/jquery.min.js',
          'media/js/main.js'
        ],
        dest: 'media/js/concat.js'
      }
    }
  });

  // Load the Grunt plugins.
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-autoprefixer');

  // Register the default tasks.
  grunt.registerTask('default', ['watch']);
};
