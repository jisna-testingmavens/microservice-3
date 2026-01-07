pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO   = "test-pipeline-repo"
        ACCOUNT_ID = "756827365110"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
                script {
                    // Get the current git commit for IMAGE_TAG
                    env.IMAGE_TAG = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    echo "Using IMAGE_TAG = ${env.IMAGE_TAG}"
                }
            }
        }

        stage("Debug Tools") {
            steps {
                sh 'docker --version || true'
                sh 'aws --version || true'
            }
        }

        stage("Build Docker Image") {
            steps {
                sh '''
                docker build -t $ECR_REPO:$IMAGE_TAG .
                '''
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
                    $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage("Push Image to ECR") {
            steps {
                sh '''
                docker tag $ECR_REPO:$IMAGE_TAG \
                    $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG

                docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage("Trigger Infra Deployment") {
            steps {
                // Trigger separate infra deployment pipeline
                build job: 'infra-pipeline',
                      parameters: [
                          string(name: 'COMMIT_ID', value: env.IMAGE_TAG)
                      ]
            }
        }
    }
}
