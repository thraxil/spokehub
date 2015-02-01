module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {                            // Task
      dist: {                            // Target
        options: {                    // Target options
          style: 'expanded'
        },
        files: {                                    // Dictionary of files
          'media/css/spokehub.css': 'media/css/sass/spokehub.scss',        // 'destination': 'source'
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
      },
      js: {
        files: [
          'assets/js/*.js',
          'Gruntfile.js'
        ],
        tasks: ['jshint']
      }
    },
    compass: {
      dist: {
        options: {
          sassDir: 'media/css/sass',
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

  // Register the default tasks.
  grunt.registerTask('default', ['watch']);
};