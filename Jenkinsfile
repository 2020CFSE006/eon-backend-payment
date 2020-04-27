pipeline {
   agent any
   environment {
       registry = "magalixcorp/k8scicd"
       
   }
   stages {   
   
   stage('Init'){
       steps{
           //checkout scm;
       script{
       env.BASE_DIR = pwd()
       env.CURRENT_BRANCH = env.BRANCH_NAME
       env.IMAGE_TAG = getImageTag(env.CURRENT_BRANCH)
       env.APP_NAME= getEnvVar('APP_NAME')
       env.IMAGE_NAME = "${APP_NAME}-app"
       }
       }
   }
      
   stage('Cleanup'){
       steps{
           sh '''
           docker rmi $(docker images -f 'dangling=true' -q) || true
           docker rmi $(docker images | sed 1,2d | awk '{print $3}') || true
           '''
       }
   }
    stage('Build Dockerimage'){
       steps{
           sh '''
            docker build -t ${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}:${RELEASE_TAG} --build-arg APP_NAME=${IMAGE_NAME}  -f app/Dockerfile app/.
           '''
       }
   }
    stage('push Dockerimage'){      
      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: "${JENKINS_DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWD']])
      {
      sh '''
      echo $DOCKER_PASSWD | docker login --username ${DOCKER_USERNAME} --password-stdin ${DOCKER_REGISTRY_URL} 
      docker push ${DOCKER_REGISTRY_URL}/${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}:${RELEASE_TAG}
      docker logout
      '''
      }
    }   
  
   stage('Deploy'){
       steps{
       withCredentials([file(credentialsId: "${JENKINS_GCLOUD_CRED_ID}", variable: 'JENKINSGCLOUDCREDENTIAL')])
       {
       sh """
           gcloud auth activate-service-account --key-file=${JENKINSGCLOUDCREDENTIAL}
           gcloud config set compute/zone asia-southeast1-a
           gcloud config set compute/region asia-southeast1
           gcloud config set project ${GCLOUD_PROJECT_ID}
           gcloud container clusters get-credentials ${GCLOUD_K8S_CLUSTER_NAME}
           chmod +x $BASE_DIR/k8s/process_files.sh
           cd $BASE_DIR/k8s/
           ./process_files.sh "$GCLOUD_PROJECT_ID" "${IMAGE_NAME}" "${DOCKER_PROJECT_NAMESPACE}/${IMAGE_NAME}:${RELEASE_TAG}" "./${IMAGE_NAME}/"
           cd $BASE_DIR/k8s/${IMAGE_NAME}/.
           kubectl apply -f $BASE_DIR/k8s/${IMAGE_NAME}/
           gcloud auth revoke --all
           """
       }
       }
      }      
      
      
       stage('Build') {
           agent {
               docker {
                   image '294069028655.dkr.ecr.ap-south-1.amazonaws.com/bits-pilani:v0.5'
               }
           }
           steps {
               // Create our project directory.
               sh 'cd /code'
               sh 'mkdir -p ${GOPATH}/src/hello-world'
               // Copy all files in our Jenkins workspace to our project directory.
               sh 'cp -r ${WORKSPACE}/* ${GOPATH}/src/hello-world'
               // Build the app.
               sh 'go build'
           }
       }
       stage('Test') {
           agent {
               docker {
                   image 'golang'
               }
           }
           steps {
               // Create our project directory.
               sh 'cd ${GOPATH}/src'
               sh 'mkdir -p ${GOPATH}/src/hello-world'
               // Copy all files in our Jenkins workspace to our project directory.
               sh 'cp -r ${WORKSPACE}/* ${GOPATH}/src/hello-world'
               // Remove cached test results.
               sh 'go clean -cache'
               // Run Unit Tests.
               sh 'go test ./... -v -short'
           }
       }
       stage('Publish') {
           environment {
               registryCredential = 'dockerhub'
           }
           steps{
               script {
                   def appimage = docker.build registry + ":$BUILD_NUMBER"
                   docker.withRegistry( '', registryCredential ) {
                       appimage.push()
                       appimage.push('latest')
                   }
               }
           }
       }
       stage ('Deploy') {
           steps {
               script{
                   def image_id = registry + ":$BUILD_NUMBER"
                   sh "ansible-playbook  playbook.yml --extra-vars \"image_id=${image_id}\""
               }
           }
       }
   }
}
