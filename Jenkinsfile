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
                    IMAGE = "$ECRURL:$VERSION"
                }
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_REGISTRY_URL}:${VERSION} .'
            }
        }       
        stage('Docker push'){
            steps{
                script{
                    // login to ECR - for now it seems that that the ECR Jenkins plugin is not performing the login as expected. I hope it will in the future.
                    sh("eval \$(aws ecr get-login --no-include-email | sed 's|https://||')")
                    // Push the Docker image to ECR
                    docker.withRegistry(ECRURL, ECRCRED)
                    {
                        docker.image(IMAGE).push()
                    }
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
