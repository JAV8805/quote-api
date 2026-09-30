pipeline {
  agent any
  options {
    timestamps()
    timeout(time: 20, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '10'))
    disableConcurrentBuilds()
  }
  environment {
    IMAGE = "quote-api:${env.BUILD_NUMBER}"
  }
  stages {
    stage('Test') {
      agent { docker { image 'python:3.12-slim'; reuseNode true } }
      environment { HOME = "${env.WORKSPACE}" }
      steps {
        sh '''
          python -m venv /tmp/venv
          . /tmp/venv/bin/activate
          pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
          PYTHONPATH=. pytest --cov=app --cov-fail-under=80 --junitxml=reports/junit.xml
        '''
      }
      post { always { junit 'reports/junit.xml' } }
    }
    stage('Build image') {
      steps { sh 'docker build -t $IMAGE .' }
    }
    stage('Smoke test') {
      steps {
        sh '''
          docker run -d --name smoke-$BUILD_NUMBER $IMAGE
          sleep 3
          docker exec smoke-$BUILD_NUMBER python -c "import urllib.request;print(urllib.request.urlopen('http://localhost:8080/health').read())"
        '''
      }
      post { always { sh 'docker rm -f smoke-$BUILD_NUMBER || true' } }
    }
    stage('Approve release') {
      when { branch 'main' }
      steps { input message: "Promote ${env.IMAGE} to UAT?", ok: 'Approve' }
    }
  }
  post {
    success { echo "Pipeline OK: ${env.IMAGE}" }
    failure { echo 'Pipeline failed - check the stage logs' }
  }
}