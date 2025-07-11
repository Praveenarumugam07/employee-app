pipeline {
    agent any

    environment {
        PROJECT_ID = 'sylvan-hydra-464904-d9'
        ZONE = 'us-central1-c'
        VM_NAME = 'employee-app-vm'
        REPO_URL = 'https://github.com/Praveenarumugam07/employee-app.git'
    }

    stages {

        stage('Checkout Code') {
            steps {
                // Checkout your repository containing startup-script.sh
                git credentialsId: 'github', url: "${REPO_URL}"
            }
        }

        stage('Create VM and Deploy App') {
            steps {
                sh '''
                echo "Creating VM and deploying app..."

                # Create VM with startup-script.sh
                gcloud compute instances create $VM_NAME \
                    --project=$PROJECT_ID \
                    --zone=$ZONE \
                    --machine-type=e2-medium \
                    --image-family=debian-11 \
                    --image-project=debian-cloud \
                    --tags=http-server \
                    --metadata-from-file startup-script=startup-script.sh
                '''
            }
        }

        stage('Allow HTTP Traffic') {
            steps {
                sh '''
                echo "Allowing HTTP traffic on port 80..."

                # Create firewall rule if not exists
                if ! gcloud compute firewall-rules list --filter="name=allow-http-80" --format="value(name)" | grep -q 'allow-http-80'; then
                    gcloud compute firewall-rules create allow-http-80 \
                        --allow tcp:80 \
                        --target-tags http-server \
                        --description="Allow HTTP traffic on port 80" \
                        --project=$PROJECT_ID
                else
                    echo "Firewall rule already exists."
                fi
                '''
            }
        }

        stage('Deployment Complete') {
            steps {
                sh '''
                echo "✅ Application deployed successfully. VM details:"
                gcloud compute instances list --filter="name=($VM_NAME)"
                '''
            }
        }

    }

    post {
        success {
            echo "✅ Deployment pipeline completed successfully. Visit your VM external IP to see the application."
        }
        failure {
            echo "❌ Deployment pipeline failed. Check logs for details."
        }
    }
}
