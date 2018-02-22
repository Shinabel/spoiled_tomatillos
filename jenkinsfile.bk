pipeline {
 agent {
  docker {
   image 'maven:3-alpine'
   args '-v /root/.m2:/root/.m2'
  }
 }
 
  stages {
   stage('Build') {
    steps {
     echo "Building"
     sh 'mvn compile -f projectcode/cs4500-spring2018-project/pom.xml'
     sh 'mvn package -f projectcode/cs4500-spring2018-project/pom.xml'
    }
   }
   stage('Test'){
    steps {
     echo "Testing"
     sh 'mvn test -f projectcode/cs4500-spring2018-project/pom.xml'
    }
   }
 }
}
