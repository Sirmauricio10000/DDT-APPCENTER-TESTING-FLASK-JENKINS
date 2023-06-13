pipeline {
    agent any
    stages {
        
        stage('Prerequisites') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Code checkout from Git') {
            steps {
                git branch: 'main', url: 'https://github.com/Sirmauricio10000/Taller_API_Appcenter'
            }
        }

        stage('Code quality check via Sonarqube/Sonarcloud') {
            steps {
                echo 'Verificando con SonarQube'
                // Realiza la verificación de calidad del código estático utilizando Sonarqube/Sonarcloud
                // Puedes utilizar los pasos y configuraciones específicos de la integración que hayas instalado
                // Agrega pasos o comenta este bloque si no necesitas realizar ninguna acción
            }
        }

        stage('API testing') {
            steps {
                sh 'pytest test_AppCenter.py'
            }
        }

        stage('Report') {
            steps {
                echo 'Escribiendo reporte'
                // Genera el reporte en el formato deseado (HTML, PDF, etc.)
                // Puedes utilizar herramientas como Allure para generar reportes de pruebas
                // Agrega pasos o comenta este bloque si no necesitas realizar ninguna acción
            }
        }
    }
}
