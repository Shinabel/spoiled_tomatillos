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
    // Tests the application and produces xml reports
    stage('Test'){
      agent {
        docker {
          image 'frolvlad/alpine-python3'
          //image 'qnib/pytest'
        }
      }
      steps {
        echo "-----------Executing python tests-----------------"
        sh 'pip3 install -r spoiled_tomatillos/tests/requirements.txt'
        sh 'cd spoiled_tomatillos/tests/ && pytest'
      }
      post {
        always {
          junit 'spoiled_tomatillos/tests/reports/results.xml'
        }
      }
    }
    // Sonarqube sending project to Sonarqube server and starting analysis
    stage('SonarQube') {
      agent {
        docker {
          image 'zaquestion/sonarqube-scanner'
        }
      }
      steps {
        echo "-----------Starting SonarQube analysis-----------------"
        withSonarQubeEnv('SonarQube') {
          sh 'sonar-scanner'
        }  
      }
    }
    // Running Sonarqube results through Quality Gate set up on server
    stage ('Quality') {
      agent {
        docker {
          image 'maven:3-alpine'
          args '-v /root/.2:/root/.m2'
        }
      }
      steps {
        echo "-----------Quality Gate Check-----------------"
        sh 'sleep 30'
        timeout(time: 10, unit: 'SECONDS') {
          retry(5) {
            script {
              def qg = waitForQualityGate()
              if (qg.status != 'OK') {
                error "Pipeline aborted due to quality gate failure: ${qg.status}"
              }
            }
          }
        }
      }
    }
  }
}

