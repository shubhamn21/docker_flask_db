read -p "Enter email: " email
read -p "Enter password: " password

curl -X POST   http://0.0.0.0:5001/auth/login/ -d "email=$email" -d "password=$password"
