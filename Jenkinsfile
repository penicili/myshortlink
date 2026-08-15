pipeline {
    agent { label 'python-agent '}

    environment {
        VENV_DIR = 'venv'
    }
    stages {
        stage("build"){
            steps{
                echo 'lagi build'
            }
        }
        stage("test"){
            steps{
                echo 'lagi test'
            }
        }
        stage("deploy"){
            steps{
                echo 'lagi deploy'
            }
        }
    }
}