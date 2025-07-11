pipeline {
    agent any

    environment {
        PROJECT = "sylvan-hydra-464904-d9"
        ZONE = "	us-central1-c"
        INSTANCE_NAME = "employee-app-vm"
        MACHINE_TYPE = "e2-medium"
        IMAGE_FAMILY = "debian-11"
        IMAGE_PROJECT = "debian-cloud"
        DB_HOST = "34.56.155.20"
        DB_USER = "new-user"
        DB_PASSWORD = "12345678"
        DB_NAME = "employee_db"
    }

    stages {
        stage('Create VM') {
            steps {
                sh '''
                echo "Creating VM instance..."
                gcloud compute instances create $INSTANCE_NAME \
                  --project=$PROJECT \
                  --zone=$ZONE \
                  --machine-type=$MACHINE_TYPE \
                  --image-family=$IMAGE_FAMILY \
                  --image-project=$IMAGE_PROJECT \
                  --tags=http-server \
                  --metadata startup-script='#! /bin/bash
                    apt update
                    apt install -y python3-pip git
                    pip3 install flask mysql-connector-python
                    git clone https://github.com/YOUR_USERNAME/employee-app.git
                    cd employee-app
                    sed -i "s/YOUR_MYSQL_IP/$DB_HOST/" app.py
                    sed -i "s/YOUR_DB_USER/$DB_USER/" app.py
                    sed -i "s/YOUR_DB_PASSWORD/$DB_PASSWORD/" app.py
                    sed -i "s/YOUR_DB_NAME/$DB_NAME/" app.py
                    nohup python3 app.py &'
                '''
            }
        }

        stage('Allow Firewall') {
            steps {
                sh '''
                echo "Allowing firewall for port 5000..."
                gcloud compute firewall-rules create allow-http-5000 \
                  --allow tcp:5000 \
                  --target-tags http-server \
                  --description "Allow port 5000" \
                  --project=$PROJECT || echo "Rule may already exist"
                '''
            }
        }

        stage('Deployment Complete') {
            steps {
                sh '''
                echo "Application deployed successfully."
                gcloud compute instances list --filter="name=($INSTANCE_NAME)"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment pipeline completed successfully.'
        }
        failure {
            echo '❌ Deployment pipeline failed.'
        }
    }
}
