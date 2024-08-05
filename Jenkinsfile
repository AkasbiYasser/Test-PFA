pipeline {
    agent any
    environment {
        ACR_NAME = 'akasbiacrpfa'
        ACR_URL = "${ACR_NAME}.azurecr.io"
        SONARQUBE_ENV = 'SonarQube'
        SONARQUBE_TOKEN = 'squ_be323c1480893e4211190de55cf4978d45266d1b'
        SLACK_CHANNEL = '#pfa'
        SLACK_WEBHOOK_URL = credentials('slack-webhook')
        JAVA_HOME = "/usr/lib/jvm/java-17-openjdk-amd64"
        PATH = "${JAVA_HOME}/bin:${env.PATH}"
        ARGOCD_SERVER = '20.164.51.113'
        ARGOCD_TOKEN = credentials('argocd-token')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AkasbiYasser/Test-PFA.git', credentialsId: 'github-token'
            }
        }
        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }
        stage('Verify Java Version') {
            steps {
                sh '''
                    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                    export PATH=$JAVA_HOME/bin:$PATH
                    java -version
                '''
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(SONARQUBE_ENV) {
                    dir('backend') {
                        sh '''
                            export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                            export PATH=$JAVA_HOME/bin:$PATH
                            sonar-scanner -Dsonar.projectKey=backend -Dsonar.sources=. -Dsonar.host.url=http://4.221.188.204:9000 -Dsonar.login=${SONARQUBE_TOKEN}
                        '''
                    }
                    dir('front-end') {
                        sh '''
                            export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                            export PATH=$JAVA_HOME/bin:$PATH
                            sonar-scanner -Dsonar.projectKey=frontend -Dsonar.sources=. -Dsonar.host.url=http://4.221.188.204:9000 -Dsonar.login=${SONARQUBE_TOKEN}
                        '''
                    }
                    dir('database') {
                        sh '''
                            export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
                            export PATH=$JAVA_HOME/bin:$PATH
                            sonar-scanner -Dsonar.projectKey=db -Dsonar.sources=. -Dsonar.host.url=http://4.221.188.204:9000 -Dsonar.login=${SONARQUBE_TOKEN}
                        '''
                    }
                }
            }
        }
        
        stage('Push Docker Images to ACR') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'ACR', passwordVariable: 'ACR_PASSWORD', usernameVariable: 'ACR_USERNAME')]) {
                        sh 'docker login ${ACR_URL} -u ${ACR_USERNAME} -p ${ACR_PASSWORD}'
                        sh 'docker push ${ACR_URL}/backend:latest'
                        sh 'docker push ${ACR_URL}/frontend:latest'
                        sh 'docker push ${ACR_URL}/mysql:latest'
                    }
                }
            }
        }
        stage('Deploy to AKS') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'aks-cluster', variable: 'KUBECONFIG')]) {
                        sh '''
                            export KUBECONFIG=$KUBECONFIG
                            kubectl apply -f k8s/backend-deployment.yaml
                            kubectl apply -f k8s/frontend-deployment.yaml
                            kubectl apply -f k8s/mysql-deployment.yaml
                        '''
                    }
                }
            }
        }
        stage('Sync with ArgoCD') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'argocd-token', variable: 'ARGOCD_AUTH_TOKEN')]) {
                        sh """
                        argocd app sync generator-app-k8s --server ${ARGOCD_SERVER} --auth-token $ARGOCD_AUTH_TOKEN --insecure
                        """
                    }
                }
            }
        }
    }
    post {
        success {
            script {
                sh 'curl -X POST -H "Content-type: application/json" --data \'{"text":"Build and deployment successful."}\' ${SLACK_WEBHOOK_URL}'
            }
        }
        failure {
            script {
                sh 'curl -X POST -H "Content-type: application/json" --data \'{"text":"Build and deployment failed."}\' ${SLACK_WEBHOOK_URL}'
            }
        }
    }
}
