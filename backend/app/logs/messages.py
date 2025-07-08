"""GENERAL LOGS"""

endpoint_hit = " API ENDPOINT HIT "
seperator = ".........................................................."
server_start = " BACKEND IS RUNNING "
mongo_connection = " CONNECTED TO  MONGODB: "
mongo_connection_fail = " MongoDB connection failed: "
validation_error = "Could not validate credentials"
# ............................................................................................................................................

""" LOGS FOR USER API'S """
successfull_signup = " User created successfully "
successfull_login = " User login successfull "
password_reset_success = "Password reset successfully"

# ERRORS
existing_email = " Email already registered "
wrong_credentials = " Incorrect username or password "
unauthorized_action = "Not authorized to perform this action"
user_not_found = "User not found"

# FOR PROFILE PIC
unsupported_file_type = "Unsupported file type. Allowed types: "
file_too_large = "File too large. Max size is "

profile_pic_updated_success = "Profile picture updated successfully"
profile_pic_not_found = "Profile picture not found"
no_profile_pic_to_delete = "No profile picture to delete"
removed_profile_pic = "Profile picture removed successfully"

# ............................................................................................................................................

""" LOGS FOR COMMENT API's """
comment_created = " Comment created successfully "
comment_retrived = " Comment retrived successfully "
comment_delete_successful = "Comment deleted successfully "
admin_comment_delete = "Comment permanently deleted by admin "
comment_update = "Comment updated successfully"


# ERRORS
account_disabled = "Account disabled"
admin_privilege = "Admin privileges required"
comment_not_found = "Comment not found"
authority_error = "Not authorized to edit this comment"
