pipeline {
    agent { label 'slave-1' }

    environment {
        VENV_DIR = 'venv'
        IMAGE_NAME = 'penicili/myshortlink'
        IMAGE_TAG = "${BUILD_NUMBER}"
        REGISTRY_HOST = '192.168.1.150:5000'
        IMAGE = "${REGISTRY_HOST}/${IMAGE_NAME}"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pip install pytest
                    pytest tests/ -v
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build \
                        -t $IMAGE:$IMAGE_TAG \
                        -t $IMAGE:latest \
                        .
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push $IMAGE:$IMAGE_TAG
                    docker push $IMAGE:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -rf $VENV_DIR'
        }

        success {
            echo 'Build, test & push berhasil!'
        }

        failure {
            echo 'Ada yang gagal, cek log stage di atas.'
        }
    }
}