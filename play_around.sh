read -p "Enter Access Token (without appostrophes) :" token
i='0'
while [ $i != 6 ]; do
echo -e "\nWhat would you like to do?"
echo "1. Show datalists"
echo "2. Create new datalist"
echo "3. Add items to datalist"
echo "4. Edit"
echo "5. Delete"
echo "6. Exit"

read -p "Choose option : " i
#clear
case "$i" in
1) curl 0.0.0.0:5001/datalists/ -H "Authorization: Bearer $token"
   ;;

2) read -p "Enter datalist name : " d_name
   curl -X POST   0.0.0.0:5001/datalists/ -d "name=$d_name" -H "Authorization: Bearer $token"
   ;;

3) curl 0.0.0.0:5001/datalists/ -H "Authorization: Bearer $token"
   read -p "Please enter datalist id : " d_id
   read -p "Enter item name : " i_name
   curl 0.0.0.0:5001/datalists/$d_id/items/ -d "name=$i_name" -H "Authorization: Bearer $token"
   ;;

4) echo -e "\nWhat would you like to edit?"
   echo "1) Datalist "
   echo "2) Item "
   read -p "Select option : " j
   case "$j" in
   1) curl 0.0.0.0:5001/datalists/ -H "Authorization: Bearer $token"
      read -p "Please enter datalist id : " d_id
      read -p "Please enter new name : " d_name
      curl -X PUT 0.0.0.0:5001/datalists/$d_id -d "name=$d_name" -H "Authorization: Bearer $token"
      echo "Datalist edited successfully !"
      ;;
   2) curl 0.0.0.0:5001/datalists/ -H "Authorization: Bearer $token"
      read -p "Please enter datalist id : " d_id
      read -p "Enter item id : " i_id 
      read -p "Enter new item name : " i_name
      curl -X PUT 0.0.0.0:5001/datalists/$d_id/items/$i_id -d "name=$i_name" -H "Authorization: Bearer $token"
      echo "Item edited successfully !"
      ;;
    *) echo "Invalid option"
      ;;
    esac
    ;;
5) echo -e "\nWhat would you like to edit?"
   echo "1) Datalist "
   echo "2) Item "
   read -p "Select option : " j
   case "$j" in
   1) curl 0.0.0.0:5001/datalists/ -H "Authorization: Bearer $token"
      read -p "Please enter datalist id : " d_id
      curl -X DELETE 0.0.0.0:5001/datalists/$d_id -H "Authorization: Bearer $token"
      echo "Datalist deleted successfully !"
      ;;
   2) curl 0.0.0.0:5001/datalists/ -H "Authorization: Bearer $token"
      read -p "Please enter datalist id : " d_id
      read -p "Enter item id : " i_id           
      curl -X DELETE 0.0.0.0:5001/datalists/$d_id/items/$i_id -H "Authorization: Bearer $token"
      echo "Item deleted successfully !"
      ;;
    *) echo "Invalid option"
      ;;
    esac
    ;;
6) echo "Exiting..."
   ;;

*) echo "Invalid option"
   ;;
esac

done
