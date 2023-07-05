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
                        env.INFRA_FLASK_VERSION = previousInfraVersionParts.join('.')
                        env.FLASK_APP_VERSION = previousFlaskVersionParts.join('.')
                    } else {
                        env.INFRA_FLASK_VERSION = "v_1.0.0"
                        env.FLASK_APP_VERSION = "v_1.0.0"
                    }
                }
            }
        }

        stage('git clone') {
            steps {
                sh 'rm -rf *'
                sh 'git clone git@github.com:sivanmarom/final_project.git'
            }
        }
        stage("build user") {
            steps {
                wrap([$class: 'BuildUser', useGitAuthor: true]) {
                    script {
                        env.BUILD_USER = BUILD_USER
                        echo ${env.BUILD_USER}
                    }
                }
            }
        }

        stage('Create S3 Buckets') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/terraform/s3') {
                    script {
                        sh 'terraform init'
                        sh 'terraform apply --auto-approve'

                        // Retrieve the bucket names
                        def flaskAppBucketName = sh(script: 'terraform output -raw flask_app_bucket_name', returnStdout: true).trim()
                        def infraFlaskBucketName = sh(script: 'terraform output -raw infra_flask_bucket_name', returnStdout: true).trim()

                        // Set environment variables with the bucket names
                        env.FLASK_APP_BUCKET_NAME = flaskAppBucketName
                        env.INFRA_FLASK_BUCKET_NAME = infraFlaskBucketName

                        echo "Flask App Bucket Name: ${env.FLASK_APP_BUCKET_NAME}"
                        echo "Infra Flask Bucket Name: ${env.INFRA_FLASK_BUCKET_NAME}"
                    }
                }
            }
        }

        stage('Create Dynamodb Tables') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/terraform/dynamodb') {
                    script{
                        sh 'terraform init'
                        sh 'terraform apply --auto-approve'

                        // Retrieve the table names
                        def flaskAppTableName = sh(script: 'terraform output -raw flask_app_table_name', returnStdout: true).trim()
                        def infraFlaskTableName = sh(script: 'terraform output -raw infra_flask_table_name', returnStdout: true).trim()

                        // Set environment variables with the table names
                        env.FLASK_APP_TABLE_NAME = flaskAppTableName
                        env.INFRA_FLASK_TABLE_NAME = infraFlaskTableName

                        echo "Flask App Table Name: ${env.FLASK_APP_TABLE_NAME}"
                        echo "Infra Flask Table Name: ${env.INFRA_FLASK_TABLE_NAME}"
                    }
                }
            }
        }

        stage('build and test infra_flask') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/infra_flask_app') {
                    sh "docker build -t infra_flask_image:${env.INFRA_FLASK_VERSION} ."
                    sh "docker run -it --name infra_flask -p 5000:5000 -d infra_flask_image:${env.INFRA_FLASK_VERSION}"
                }
                dir('/var/lib/jenkins/workspace/deployment/final_project/tests'){
                    script{
                        sh 'pytest infra_test.py::Test_class --html=infra_report.html'
                        def log_entry_infra = sh(script: 'python3.8 parse_log_infra.py', returnStdout: true).trim()
                        def (timestamp, message) = log_entry_infra.split(',')
                        env.INFRA_TIMESTAMP = timestamp.trim()
                        env.INFRA_MESSAGE = message.trim().replaceAll('"', '\\"')             
                        echo "Infra Timestamp: ${env.INFRA_TIMESTAMP}"
                        echo "Infra Message: ${env.INFRA_MESSAGE}"
                    }
                }
            }
        }

        stage('build and test flask_app') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project') {
                    sh "docker build -t flask_app_image:${env.FLASK_APP_VERSION} ."
                    sh "docker run -it --name flask_app -p 5001:5001 -d flask_app_image:${env.FLASK_APP_VERSION}"
                }
                dir('/var/lib/jenkins/workspace/deployment/final_project/tests'){
                    script{
                        sh 'pytest flask_test.py::Test_class --html=flask_report.html'
                        def log_entry_flask = sh(script: 'python3.8 parse_log_flask.py', returnStdout: true).trim()
                        def (timestamp, message) = log_entry_flask.split(',')
                        env.FLASK_TIMESTAMP = timestamp.trim()
                        env.FLASK_MESSAGE = message.trim().replaceAll('"', '\\"')             
                        echo "flask Timestamp: ${env.FLASK_TIMESTAMP}"
                        echo "flask Message: ${env.FLASK_MESSAGE}"
                    }
                }
            }
        }

        stage('upload to s3 bucket') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/tests') {
                    withAWS(credentials: 'aws-credentials') {
                        sh "aws s3 cp flask_report.html s3://${env.FLASK_APP_BUCKET_NAME}"
                        sh "aws s3 cp infra_report.html s3://${env.INFRA_FLASK_BUCKET_NAME}"
                    }
                }
            }
        }

        stage('Upload to dynamodb') {
            steps {
                dir('/var/lib/jenkins/workspace/deployment/final_project/tests') {
                    script {
                        withAWS(credentials: 'aws-credentials', region: 'us-west-2') {
                            sh "aws dynamodb put-item --table-name env.INFRA_FLASK_TABLE_NAME --item \"{\\\"User\\\": {\\\"S\\\": \\\"${env.BUILD_USER}\\\"}, \\\"Timestamp\\\": {\\\"S\\\": \\\"${env.INFRA_TIMESTAMP}\\\"}, \\\"Message\\\": {\\\"S\\\": \\\"${env.INFRA_MESSAGE}\\\"}}\""
                        }
                        withAWS(credentials: 'aws-credentials', region: 'us-west-2') {
                            sh "aws dynamodb put-item --table-name env.FLASK_APP_TABLE_NAME --item \"{\\\"User\\\": {\\\"S\\\": \\\"${env.BUILD_USER}\\\"}, \\\"Timestamp\\\": {\\\"S\\\": \\\"${env.FLASK_TIMESTAMP}\\\"}, \\\"Message\\\": {\\\"S\\\": \\\"${env.FLASK_MESSAGE}\\\"}}\""
                        }
                    }
                }
            }
        }

        // stage('push to dockerhub infra_app') {
        //     steps {
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
        //             sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
        //             sh "docker tag infra_flask_image:${env.INFRA_FLASK_VERSION} sivanmarom/infra_flask:${env.INFRA_FLASK_VERSION}"
        //             sh "docker push sivanmarom/infra_flask:${env.INFRA_FLASK_VERSION}"
        //         }
        //     }
        // }

        // stage('push to dockerhub flask_app') {
        //     steps {
        //         sh "docker tag flask_app_image:${env.FLASK_APP_VERSION} sivanmarom/flask_app:${env.FLASK_APP_VERSION}"
        //         sh "docker push sivanmarom/flask_app:${env.FLASK_APP_VERSION}"
        //     }
        // }

        // stage('create EKS cluster') {
        //     steps {
        //         dir('/var/lib/jenkins/workspace/deployment/final_project/terraform/eks') {
        //             sh 'terraform init'
        //             sh 'terraform apply --auto-approve'
        //             sh 'eksctl utils write-kubeconfig --cluster=eks-cluster'
        //             sh 'kubectl get nodes'
        //         }
        //     }
        // }

        // stage('Helm Chart') {
        //     steps {
        //         dir('/var/lib/jenkins/workspace/deployment/final_project/k8s/mychart') {
        //             script {
        //                 def imageTagFlask = env.FLASK_APP_VERSION
        //                 def imageTagInfra = env.INFRA_FLASK_VERSION

        //                 sh 'kubectl apply -f namespace.yaml'

        //                 // Update values.yaml with image tag parameters
        //                 sh "sed -i 's/tag: latest/tag: ${imageTagFlask}/' values.yaml"
        //                 sh "sed -i 's/tag: latest/tag: ${imageTagInfra}/' values.yaml"
        //                 sh "cat values.yaml"
        //                 // Build your Helm chart
        //                 sh 'helm package .'
        //                 sh "helm upgrade --install mychart mychart-0.1.0.tgz --namespace apps-space -f values.yaml"
        //             }
        //         }
        //     }
        // }

        // stage('Apps Deploy') {
        //     steps {
        //         dir('/var/lib/jenkins/workspace/deployment/final_project/k8s/mychart/templates') {
        //             script {
        //                 sh 'kubectl apply -f infra-flask-deployment.yaml'
        //                 sh 'kubectl apply -f flask-app-deployment.yaml'
        //                 sh 'kubectl get all --namespace apps-space'
        //             }
        //         }
        //     }
        // }        
    }
    post {
        always {
            deleteDir()
        }
    }
}

