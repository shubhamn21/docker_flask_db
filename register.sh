read -p "Enter first name: " firstname
read -p "Enter last name: " lastname
read -p "Enter email: " email
read -p "Enter password (longer than 8): " password

# Register user
curl -X POST   http://0.0.0.0:5001/auth/register/ -d "first_name=$firstname" -d "second_name=$lastname" -d "email=$email" -d "password=$password"
