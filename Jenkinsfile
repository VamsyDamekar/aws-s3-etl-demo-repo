pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:${env.PATH}" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Check Environment') {
            steps {
                sh '''
                    echo "PATH is: $PATH"
                    which terraform || echo "terraform not found"
                    terraform -version || echo "terraform command failed"
                '''
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
                        /opt/homebrew/bin/terraform init
                        echo "Applying Terraform..."
                        /opt/homebrew/bin/terraform apply -auto-approve
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
