pipeline {
    agent any
    
    stages {
        stage('Initialize version') {
            steps {
                script {
                        if (currentBuild.previousBuild != null && currentBuild.previousBuild.result == 'SUCCESS') {
                            def previousInfraVersionParts = currentBuild.previousBuild.buildVariables.INFRA_FLASK_VERSION.split('\\.')
                            def previousFlaskVersionParts = currentBuild.previousBuild.buildVariables.FLASK_APP_VERSION.split('\\.')

                            // Incrementing the last part of the version
                            previousInfraVersionParts[-1] = (previousInfraVersionParts[-1] as int) + 1
                            previousFlaskVersionParts[-1] = (previousFlaskVersionParts[-1] as int) + 1

                            // Joining the version parts back into a string
                            env.INFRA_FLASK_VERSION = 'v' + previousInfraVersionParts.join('.')
                            env.FLASK_APP_VERSION = 'v' + previousFlaskVersionParts.join('.')
                        } else {
                            env.INFRA_FLASK_VERSION = 'v1.0.0'
                            env.FLASK_APP_VERSION = 'v1.0.0'
            }

                            echo "Current versions:"
                            echo "INFRA_FLASK_VERSION: ${env.INFRA_FLASK_VERSION}"
                            echo "FLASK_APP_VERSION: ${env.FLASK_APP_VERSION}"
                }    
            }
        }
        
        stage('git clone') {
            steps {
                sh 'rm -rf *'
                sh 'git clone git@github.com:sivanmarom/final_project.git'
            }
        }

                stage('build and test infra_flask') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/infra_flask_app') {
                    sh "docker build -t infra_flask_image:${env.INFRA_FLASK_VERSION} ."
                    sh "docker run -it --name infra_flask -p 5000:5000 -d infra_flask_image:${env.INFRA_FLASK_VERSION}"
                }
            }
        }

        stage('build and test flask_app') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project') {
                    sh "docker build -t flask_app_image:${env.FLASK_APP_VERSION} ."
                    sh "docker run -it --name flask_app -p 5001:5001 -d flask_app_image:${env.FLASK_APP_VERSION}"
                }
            }
        }

        stage('push to dockerhub infra_app') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                    sh "docker tag infra_flask_image:${env.INFRA_FLASK_VERSION} sivanmarom/infra_flask:${env.INFRA_FLASK_VERSION}"
                    sh "docker push sivanmarom/infra_flask:${env.INFRA_FLASK_VERSION}"
                }
            }
        }

        stage('push to dockerhub flask_app') {
            steps {
                sh "docker tag flask_app_image:${env.FLASK_APP_VERSION} sivanmarom/flask_app:${env.FLASK_APP_VERSION}"
                sh "docker push sivanmarom/flask_app:${env.FLASK_APP_VERSION}"
            }
        }

        stage('create EKS cluster') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/terraform/eks') {
                    sh 'terraform init'
                    sh 'terraform apply --auto-approve'
                    sh 'eksctl utils write-kubeconfig --cluster=eks-cluster'
                    sh 'kubectl get nodes'
                }
            }
        }

        stage('apps deploy') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/k8s') {
                    script {
                     def imageTag_flask = env.FLASK_APP_VERSION
                     def imageTag_infra =env.INFRA_FLASK_VERSION
                     sh "sed -i 's#PLACEHOLDER_INFRA#${imageTag_infra}#g' infra-flask-deployment.yaml"
                     sh "sed -i 's#PLACEHOLDER_FLASK#${imageTag_flask}#g' flask-app-deployment.yaml"
                     sh "cat flask-app-deployment.yaml"
                      sh "cat infra-flask-deployment.yaml"

                        sh 'kubectl apply -f infra-flask-deployment.yaml'
                        sh 'kubectl apply -f flask-app-deployment.yaml'
                        sh 'kubectl get all --namespace flask-space'
                    }
                }
            }
        }

    }
}
