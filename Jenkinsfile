pipeline {
    agent any

    environment {
        PATH = "/opt/homebrew/bin:${env.PATH}" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh '''
                        echo "Initializing Terraform..."
                        terraform init
                        echo "Applying Terraform..."
                        terraform apply -auto-approve
                    '''
                }
            }
        }

        stage('Run Python ETL Script') {
            steps {
                sh '''
                    echo "Running ETL Python script..."
                    python3 my_script.py
                '''
            }
        }

        stage('Upload Output to S3') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh '''
                        echo "Uploading transformed file to S3..."
                        aws s3 cp output/transformed.csv s3://curatedbts3/
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully ✅'
        }
        failure {
            echo 'Pipeline failed ❌'
        }
    }
}
