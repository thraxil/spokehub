module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt);
  require('time-grunt')(grunt);

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
      dist: {
        options: {style: 'compact', sourcemap: 'none'},
        files: {'media/dist/styles/spokehub.css': 'media/preprocess/styles/spokehub.scss'}
      }
    },
    postcss: {
      options: {
        map: false,
        processors: [require('autoprefixer-core')({browsers: 'last 2 versions'})]
      },
      dist: {src: 'media/dist/styles/spokehub.css'}
    },
    jshint: {
      dist: ['Gruntfile.js','media/preprocess/js/app.js']
    },
    uglify: {
      options: {
        mangle: {except:['jQuery']}
      },
      dist:{
        files: {
          'media/dist/js/app.js' : ['media/preprocess/js/app.js']
        }
      }
    },
    bower: {
      dist: {
        options: {
          keepExpandedHierarchy: false,
          packageSpecific: {
            'jquery': {
              files: ['dist/jquery.min.js']
            }
          }
        },
        dest:'media/',
        js_dest: 'media/dist/js',
        scss_dest: 'media/preprocess/styles/vendor',
        fonts_dest: 'media/dist/fonts'
      }
    },
    watch: {
      css: {
        files: ['media/preprocess/styles/**/*.scss'],
        tasks: ['sass','postcss']
      },
      js: {
        files: ['media/preprocess/js/*.js'],
        tasks: ['jshint','uglify']
      }
    }
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('build', ['bower','sass','postcss','uglify']);
};
