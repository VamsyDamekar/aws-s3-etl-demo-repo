pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-creds')
        AWS_SECRET_ACCESS_KEY = credentials('aws-creds')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Running build...'
            }
        }
        stage('Deploy to S3') {
            steps {
                sh '''
                    aws s3 ls
                    aws s3 cp app.txt s3://curatedbts3/
                   '''
            }
        }
    }
}

