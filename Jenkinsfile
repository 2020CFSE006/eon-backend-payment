pipeline {
   agent any
   environment {
       DOCKER_REGISTRY_URL = "294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani"
       RELEASE_TAG = "0.5"
   }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_REGISTRY_URL}:${RELEASE_TAG} -f app/Dockerfile app/.'
            }
        }
        stage('Pushing to S3') {
            steps {
                sh 'aws s3 rm s3://${bucket_name}  --recursive'
                sh 'aws s3 sync build/ s3://${bucket_name}'
            }
        }
        stage('Cloudfront invalidation') {
            steps {
                sh 'aws cloudfront create-invalidation  --distribution-id ${cloudfront_distro_id}  --paths "/*"'
            }
        }
    }
}
