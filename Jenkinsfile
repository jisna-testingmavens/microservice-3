pipeline {
  agent any

  environment {
    AWS_REGION = "us-east-1"
    ECR_REPO   = "test-pipeline-repo"
    COMMIT_ID  = "${GIT_COMMIT}"
  }

  stages {

    stage("Checkout") {
      steps {
        checkout scm
      }
    }

    stage("Build Docker Image") {
      steps {
        sh "docker build -t $ECR_REPO:$COMMIT_ID ."
      }
    }

    stage("Login to ECR") {
      steps {
        withCredentials([[
          $class: 'AmazonWebServicesCredentialsBinding',
          credentialsId: 'test-pipeline-creds'
        ]]) {
          sh '''
          aws ecr get-login-password --region $AWS_REGION | \
          docker login --username AWS --password-stdin \
          $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com
          '''
        }
      }
    }

    stage("Push Image") {
      steps {
        sh '''
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

        docker tag $ECR_REPO:$COMMIT_ID \
          $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$COMMIT_ID

        docker push \
          $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$COMMIT_ID
        '''
      }
    }
  }
}
