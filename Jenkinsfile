pipeline {
    agent any

    environment {
        PROJECT_ID = 'sylvan-hydra-464904-d9'
        ZONE = 'us-central1-c'
        VM_NAME = 'employee-app-vm'
        REPO_URL = 'https://github.com/Praveenarumugam07/employee-app.git'
    }

    stages {

        stage('Create VM and Deploy App') {
            steps {
                sh '''
                echo "Creating VM and deploying app..."

                gcloud compute instances create $VM_NAME \
                    --project=$PROJECT_ID \
                    --zone=$ZONE \
                    --machine-type=e2-medium \
                    --image-family=debian-11 \
                    --image-project=debian-cloud \
                    --tags=http-server \
                    --metadata=startup-script='#! /bin/bash
                    apt update
                    apt install -y python3-pip git
                    pip3 install flask mysql-connector-python

                    # Clone repo
                    git clone ${REPO_URL}
                    cd employee-app

                    # Install requirements if requirements.txt exists
                    if [ -f "requirements.txt" ]; then
                        pip3 install -r requirements.txt
                    fi

                    # Replace DB details if needed
                    # sed -i "s/YOUR_MYSQL_IP/$DB_HOST/" app.py

                    # Modify app.py to run on port 80 (requires root)
                    sed -i "s/app.run(/app.run(host=\"0.0.0.0\", port=80, /" app.py

                    # Run app on port 80
                    nohup python3 app.py &
                    '
                '''
            }
        }

        stage('Allow HTTP Traffic') {
            steps {
                sh '''
                echo "Allowing HTTP traffic on port 80..."

                # Create firewall rule if not existing
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
                echo "Application deployed successfully."
                echo "VM details:"
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
