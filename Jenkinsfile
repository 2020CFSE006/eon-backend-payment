pipeline {
   agent any
   environment {
      AWS_DEFAULT_REGION = "ap-south-1"
      AWS_ACCOUNT_ID = "294069028655"
      IMAGE_REPO_NAME = "bits-pilani"
      BUILD_ID = "4.0" //"1.${currentBuild.number}"
      EKS_KUBECTL_ROLE_ARN = 'arn:aws:iam::294069028655:role/bits-pilani'

            
      
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
       
        stage(' deploy kubectl and helm packages ') {
            steps {
                sh 'curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.12.0/bin/linux/amd64/kubectl'
                sh 'curl -sS -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.13.7/2019-06-11/bin/linux/amd64/aws-iam-authenticator'
                sh 'chmod +x ./kubectl ./aws-iam-authenticator'
                sh 'export PATH=$PWD/:$PATH'
                sh 'export KUBECONFIG=$HOME/.kube/config'
                sh 'wget https://get.helm.sh/helm-v2.16.3-linux-amd64.tar.gz'
                sh 'tar -zxvf helm-v2.16.3-linux-amd64.tar.gz'
                sh 'cd linux-amd64 && sudo  mv helm /usr/local/bin/ && cd ..'
              
            }
        }
       
        stage('eks authentication and deploy kubectl and helm packages ') {
            steps {
                sh 'aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION'
                //sh 'aws sts assume-role --role-arn $EKS_KUBECTL_ROLE_ARN  --role-session-name demo-kubectl --duration-seconds 900'
                sh 'aws eks --region $AWS_DEFAULT_REGION update-kubeconfig --name bits-pilani-eon'
               sh 'kubectl get nodes'
                sh 'helm ls'
            }
        }
    }
}
