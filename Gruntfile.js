module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concagrut: {
      dist: {
        src: [
        'media/components/jquery/dist/jquery.min.js',
        'media/components/bootstrap/dist/js/bootstrap.min.js'
        ],
        dest: 'media/js/concat.js'
      }
      },
    sass: {                            // Task
      dist: {                            // Target
        options: {                    // Target options
          style: 'expanded'
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
        tasks: ['sass']
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
      options: {
        jshintrc: '.jshintrc'
      },
      all: ['Gruntfile.js', 'assets/js/*.js']
    }
  });

  // Load the Grunt plugins.
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-concat');

  // Register the default tasks.
  grunt.registerTask('default', ['watch']);
};
