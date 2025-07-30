pipeline {
  agent none
  options {
    timestamps()
  }
  stages {
    stage('build') {
      parallel {
        stage('fedora-41') {
          agent { label 'fedora-41-rpm' }
          steps {
            sh 'sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_41/devel:languages:crystal.repo'
            sh 'rpmtool build invidious.spec'
          }
        }
        stage('fedora-42') {
          agent { label 'fedora-42-rpm' }
          steps {
            sh 'sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_42/devel:languages:crystal.repo'
            sh 'rpmtool build invidious.spec'
          }
        }
      }
    }
  }
  post {
    failure {
      emailext(
        to: '$DEFAULT_RECIPIENTS',
        subject: '$DEFAULT_SUBJECT',
        body: '$DEFAULT_CONTENT',
      )
    }
    fixed {
      emailext(
        to: '$DEFAULT_RECIPIENTS',
        subject: '$DEFAULT_SUBJECT',
        body: '$DEFAULT_CONTENT',
      )
    }
  }
}
