pipeline {
   agent any
   environment {
       DOCKER_REGISTRY_URL = "294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani"
       RELEASE_TAG = "0.5"
       PROJECT = 'eon_payment'
       ECRURL = 'http://294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani'
       ECRCRED = 'ecr:eu-central-1:tap_ecr'
      AWS_DEFAULT_REGION = "ap-south-1"
      AWS_ACCOUNT_ID = "294069028655"
      IMAGE_REPO_NAME = "bits-pilani"
      CODEBUILD_BUILD_NUMBER = sh "previous build number: ${currentBuild.previousBuild.getNumber()}"
      COMMIT_HASH = sh "current build number: ${currentBuild.number}"
            
      
   }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_REPO_NAME:$CODEBUILD_BUILD_NUMBER-$COMMIT_HASH .'
                sh 'docker tag $IMAGE_REPO_NAME:$CODEBUILD_BUILD_NUMBER-$COMMIT_HASH  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$CODEBUILD_BUILD_NUMBER-$COMMIT_HASH'
            }
        }       
        stage('Docker push'){
            steps{
                script{
                    // login to ECR - for now it seems that that the ECR Jenkins plugin is not performing the login as expected. I hope it will in the future.
                    sh("eval \$(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)")

                      sh 'echo Build completed on `date`'
                      sh 'echo Pushing the Docker images...'
                      sh 'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$CODEBUILD_BUILD_NUMBER-$COMMIT_HASH'

                    //}
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
