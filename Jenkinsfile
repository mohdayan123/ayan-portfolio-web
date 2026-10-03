pipeline{
    agent any
    
    stages{
        stage("Code Clone"){
            steps{
                git url: "https://github.com/mohdayan123/ayan-portfolio-web.git/", branch: "main" 
            }
        }
        stage("Test"){
            steps{
                echo "Testing Completed"
            }
        }
        stage("Build"){
            steps{
                sh "docker build -t ayan-portfolio-image ."
            }
        }
        stage("Docker Hub"){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: "dockerHubCreds",
                    passwordVariable: "dockerHubPass",
                    usernameVariable: "dockerHubUser"
                    )]){
                sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                sh "docker image tag ayan-portfolio-image ${env.dockerHubUser}/ayan-portfolio-image"
                sh "docker push ${env.dockerHubUser}/ayan-portfolio-image "
                    }
            }
        }
        stage("Deploy"){
            steps{
                sh "docker compose up -d --build"
            }
        }
        
    }
}
