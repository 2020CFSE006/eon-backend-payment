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
      CODEBUILD_BUILD_NUMBER = "1"
      COMMIT_HASH = "2"
   }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_REPO_NAME:$CODEBUILD_BUILD_NUMBER-$COMMIT_HASH .'
            }
        }       
        stage('Docker push'){
            steps{
                script{
                    // login to ECR - for now it seems that that the ECR Jenkins plugin is not performing the login as expected. I hope it will in the future.
                    sh("eval \$(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)")
                   //sh("eval \$(aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani)")
                   
                    // Push the Docker image to ECR
                   // docker.withRegistry('http://294069028655.dkr.ecr.ap-south-1.amazonaws.com','ecr:ap-south-1:aws-creds') {
          
                     //build image
                  //   def customImage = docker.build("bits-pilani:${env.BUILD_ID}")
                      sh 'echo Build completed on `date`'
                      sh 'echo Pushing the Docker images...'
                      sh 'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$CODEBUILD_BUILD_NUMBER-$COMMIT_HASH'
                     //push image
                     //customImage.push()
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
