pipeline {
    agent { label 'slave-1' }

    environment {
        VENV_DIR = 'venv'
        IMAGE_NAME= 'penicili/myshortlink'
        IMAGE_TAG= "${BUILD_NUMBER}"
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
                    docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:latest .
                '''
            }
        }
        
        stage ('Push Image to dockerhub'){
            steps{
                withCredentials([usernamePassword(credentialsId: 'dockerhub-pat', usernameVariable: 'HUB_USER', passwordVariable: 'HUB_PASSWORD')]){
                    sh '''
                        echo DOCKER_PASS | docker login -u $HUB_USER --password-stdin
                        docker push $IMAGE_NAME:$IMAGE_TAG
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }
        
        stage ('Deploy')
            steps{
                echo "ya nanti di deploy lah gimana gitu pokonya anu lah"
            }
    }

    post {
        always {
            sh 'rm -rf $VENV_DIR'
        }
        success {
            echo 'Build & test berhasil!'
        }
        failure {
            echo 'Ada yang gagal, cek log stage di atas.'
        }
    }
}