pipeline {
   agent any
   environment {
       DOCKER_REGISTRY_URL = "294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani"
       RELEASE_TAG = "0.5"
       PROJECT = 'eon_payment'
       ECRURL = 'http://294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani'
       ECRCRED = 'ecr:eu-central-1:tap_ecr'
   }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_REGISTRY_URL}:${RELEASE_TAG} .'
            }
        }
        stage('Build preparations'){
            steps{
                script{
                    // calculate GIT lastest commit short-hash
                    gitCommitHash = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    shortCommitHash = gitCommitHash.take(7)
                    // calculate a sample version tag
                    VERSION = shortCommitHash
                    // set the build display name
                    currentBuild.displayName = "#${BUILD_ID}-${VERSION}"
                    IMAGE = "$PROJECT:$VERSION"
                }
            }
        }
        stage('Docker build'){
            steps{
                script{
                    // Build the docker image using a Dockerfile
                    docker.build("$IMAGE","examples/pipelines/TAP_docker_image_build_push_ecr")
                }
            }
        }
        stage('Cloudfront invalidation') {
            steps {
                sh 'aws cloudfront create-invalidation  --distribution-id ${cloudfront_distro_id}  --paths "/*"'
            }
        }
    }
}
