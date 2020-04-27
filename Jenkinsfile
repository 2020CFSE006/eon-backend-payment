pipeline {
   agent any
   environment {
      AWS_DEFAULT_REGION = "ap-south-1"
      AWS_ACCOUNT_ID = "294069028655"
      IMAGE_REPO_NAME = "bits-pilani"
      BUILD_ID = "4.0" //"1.${currentBuild.number}"
      EKS_KUBECTL_ROLE_ARN1 = 'arn:aws:iam::294069028655:role/bits-pilani'

            
      
   }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_REPO_NAME:$BUILD_ID .'
                sh 'docker tag $IMAGE_REPO_NAME:$BUILD_ID  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$BUILD_ID'
            }
        }       
        stage('Docker push'){
            steps{
                script{
                    // login to ECR - for now it seems that that the ECR Jenkins plugin is not performing the login as expected. I hope it will in the future.
                    sh("eval \$(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)")

                      sh 'echo Build completed on `date`'
                      sh 'echo Pushing the Docker images...'
                      sh 'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$BUILD_ID'
                      sh 'echo code pushed on `date`'
                    //}
                }
            }
        }
        stage('eks authentication') {
            steps {
                sh 'aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION'
                sh 'aws sts assume-role --role-arn $EKS_KUBECTL_ROLE_ARN  --role-session-name codebuild-kubectl --duration-seconds 900'
            }
        }
    }
}
