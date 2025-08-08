pipeline {
    agent any

    environment {
        PATH+EXTRA = "/usr/local/bin:/opt/homebrew/bin"
    }

    stages {
        stage('Verify Environment') {
            steps {
                sh '''
                    echo "PATH is: $PATH"
                    which terraform || echo "terraform not found"
                    terraform -version || echo "terraform version command failed"
                    which python3 || echo "python3 not found"
                    python3 --version || echo "python3 version command failed"
                    which aws || echo "aws cli not found"
                    aws --version || echo "aws version command failed"
                '''
            }
        }

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
