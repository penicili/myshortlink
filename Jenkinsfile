pipeline {
    agent { label 'python-agent' }

    environment {
        VENV_DIR = 'venv'
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

        stage('Build Verification') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    python -c "import main; print('Import OK')"
                '''
            }
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