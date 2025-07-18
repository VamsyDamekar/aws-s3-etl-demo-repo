pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:${env.PATH}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Running build...'
            }
        }

        stage('Deploy to S3') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']
                ]) {
                    sh '''
                        aws s3 ls
                        aws s3 cp Hey.txt s3://curatedbts3/
                    '''
                }
            }
        }
    }
}
