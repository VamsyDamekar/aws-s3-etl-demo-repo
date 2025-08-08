pipeline {
    agent any

    environment {
    PATH+EXTRA = "/opt/homebrew/bin:/usr/local/bin"
}

    stages {
        stage('Verify Tools') {
            steps {
                sh '''
                    echo "PATH=$PATH"
                    which terraform || echo "terraform not found"
                    ${TERRAFORM_PATH} -version || echo "terraform command failed"
                    which python3 || echo "python3 not found"
                    python3 --version || echo "python3 command failed"
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
                        ${TERRAFORM_PATH} init
                        echo "Applying Terraform..."
                        ${TERRAFORM_PATH} apply -auto-approve
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
