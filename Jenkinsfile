// Initial Pipeline declaration
pipeline {
  // Must specifiy agent for each stage
  agent none
  stages {
      // Builds the application
      stage('Build') {
        agent {
          docker {
            image 'frolvlad/alpine-python3'
          }
        }
        steps {
          echo '-------------Executing build stage------------' 
        }
      }

      // Tests the application
      stage('Test'){
        agent {
          image 'frolvlad/alpine-python3'
        }        
        steps {
          echo "-----------Executing python tests-----------------"
          sh 'python3 spoiled_tomatillos/app/tests/flaskr_tests.py'
        }
      }
    }
  }
}
