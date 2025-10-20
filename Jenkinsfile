pipeline {
  agent none
  options {
    timestamps()
  }
  stages {
    stage('build') {
      parallel {
        stage('fedora-41-x86_64') {
          agent {
            node {
              label 'fedora-41-rpm-large-isolated'
              customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
            }
          }
          steps {
            sh '''
              sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_41/devel:languages:crystal.repo
              rpmtool build invidious.spec
              mkdir --parents "${WORKSPACE}/artifacts/fedora/41"
              mv "${HOME}/rpmbuild/SRPMS" "${WORKSPACE}/artifacts/fedora/41/"
              mv "${HOME}/rpmbuild/RPMS" "${WORKSPACE}/artifacts/fedora/41/"
            '''
            stash includes: 'artifacts/fedora/41/**/*', name: 'fedora-41-x86_64'
          }
        }
        stage('fedora-42-x86_64') {
          agent {
            node {
              label 'fedora-42-rpm-large-isolated'
              customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
            }
          }
          steps {
            sh '''
              sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_42/devel:languages:crystal.repo
              rpmtool build invidious.spec
              mkdir --parents "${WORKSPACE}/artifacts/fedora/42"
              mv "${HOME}/rpmbuild/SRPMS" "${WORKSPACE}/artifacts/fedora/42/"
              mv "${HOME}/rpmbuild/RPMS" "${WORKSPACE}/artifacts/fedora/42/"
            '''
            stash includes: 'artifacts/fedora/42/**/*', name: 'fedora-42-x86_64'
          }
        }
        stage('rocky-10-x86_64') {
          agent {
            node {
              label 'rocky-10-rpm-large-isolated'
              customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
            }
          }
          steps {
            sh '''
              sudo wget --directory-prefix=/etc/yum.repos.d https://download.opensuse.org/repositories/devel:/languages:/crystal/Fedora_Rawhide/devel:languages:crystal.repo
              rpmtool build invidious.spec
              mkdir --parents "${WORKSPACE}/artifacts/rocky/10"
              mv "${HOME}/rpmbuild/SRPMS" "${WORKSPACE}/artifacts/rocky/10/"
              mv "${HOME}/rpmbuild/RPMS" "${WORKSPACE}/artifacts/rocky/10/"
            '''
            stash includes: 'artifacts/rocky/10/**/*', name: 'rocky-10-x86_64'
          }
        }
      }
    }
    stage('publish') {
      agent {
        node {
          label 'fedora-42'
          customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
        }
      }
      steps {
        unstash 'fedora-41-x86_64'
        unstash 'fedora-42-x86_64'
        unstash 'rocky-10-x86_64'
        archiveArtifacts artifacts: 'artifacts/**/*', fingerprint: true, onlyIfSuccessful: true
      }
    }
    stage('copr') {
      agent {
        node {
          label 'fedora-42-rpm'
          customWorkspace "${env.JOB_NAME}/${env.BUILD_ID}"
        }
      }
      when {
        allOf {
          expression { params.COPR_BUILD == true }
          expression { env.GIT_BRANCH == 'origin/master' }
        }
      }
      steps {
        withCredentials([file(credentialsId: 'pgdev-copr-api', variable: '__COPR_API_CONFIG')]) {
          sh '''
            copr --config "$__COPR_API_CONFIG" build-package --nowait --background --name invidious pgdev/invidious
          '''
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
