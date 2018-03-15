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
          image 'qnib/pytest'
        }
      }
      steps {
        echo "-----------Executing python tests-----------------"
        sh 'pytest --verbose --junit-xml test-reports/results.xml spoiled_tomatillos/app/tests/flaskr_tests.py'
      }
      post {
        always {
          junit 'test-reports/results.xml'
        }
      }
    }
    // Sonarqube sending project to Sonarqube server and starting analysis
    stage('SonarQube') {
      agent {
        docker {
          image 'maven:3-alpine'
          args '-v /root/.2:/root/.m2'
        }
      }
      steps {
        echo "-----------Starting SonarQube analysis-----------------"
        withSonarQubeEnv('SonarQube') {
          sh '(cd projectcode/cs4500-spring2018-project/ && mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent install -Dmaven.test.failure.ignore=true)'
          sh '(cd projectcode/cs4500-spring2018-project/ && mvn sonar:sonar -Dsonar.host.url=http://ec2-18-220-143-170.us-east-2.compute.amazonaws.com:9000/)'
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

