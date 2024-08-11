pipeline {
  agent none
  options {
    timestamps()
  }
  stages {
    stage('build') {
      parallel {
        stage('fedora-39') {
          agent { label 'fedora-39-rpm' }
          steps {
            sh 'sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_39/devel:languages:crystal.repo'
            sh 'rpmtool rpm invidious.spec'
          }
        }
        stage('fedora-40') {
          agent { label 'fedora-40-rpm' }
          steps {
            sh 'sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_40/devel:languages:crystal.repo'
            sh 'rpmtool rpm invidious.spec'
          }
        }
      }
    }
  }
}
