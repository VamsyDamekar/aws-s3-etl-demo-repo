pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Running build...'
            }
        }

        stage('Deploy to S3') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh '''
                        /usr/local/bin/aws s3 ls
                        /usr/local/bin/aws s3 cp app.txt s3://curatedbts3/
                    '''
                }
            }
        }
    }
}
