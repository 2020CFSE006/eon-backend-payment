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
        stage('Docker push'){
            steps{
                script{
                    // login to ECR - for now it seems that that the ECR Jenkins plugin is not performing the login as expected. I hope it will in the future.
                   // sh("eval \$(aws ecr get-login --no-include-email | sed 's|https://||')")
                   //sh("eval \$(aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani)")
                   
                    // Push the Docker image to ECR
                    docker.withRegistry('http://294069028655.dkr.ecr.ap-south-1.amazonaws.com','ecr:ap-south-1:c81caff0-7898-4f59-b495-a396e607f7fd') {
          
                     //build image
                     def customImage = docker.build("bits-pilani:${env.BUILD_ID}")

                     //push image
                     customImage.push()
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
