field_user = ("id",
              "email",
			  "is_active",
			  "is_superuser",
			  "is_verified",
              "username",
              "register_ref_code")


data_for_create_user = {
  "email": "artyukovskiikirill@gmail.com",
  "username": "string",
  "password": "string"
}


data_for_create_user_by_ref_code = {
  "email": "artyukovskii@gmail.com",
  "username": "string",
  "password": "string"
}


data_for_login = {
	"username": "artyukovskiikirill@gmail.com",
	"password": "string"
}
