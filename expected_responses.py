# Коды ответов
SUCCESS_CODE = 200
BAD_REQUEST_CODE = 400
UNAUTHORIZED_CODE = 401
FORBIDDEN_CODE = 403
SERVER_ERROR_CODE = 500

# Ожидаемые ответы для различных сценариев
REGISTER_SUCCESS = "accessToken"
REGISTER_USER_EXISTS = {"success": False, "message": "User already exists"}
REGISTER_MISSING_FIELD = {"success": False, "message": "Email, password and name are required fields"}

LOGIN_SUCCESS = {"success": True}
LOGIN_FAILED = {"success": False, "message": "email or password are incorrect"}

UPDATE_USER_SUCCESS = {"success": True}
UPDATE_USER_UNAUTHORIZED = {"success": False, "message": "You should be authorised"}
UPDATE_USER_EXISTS = {"success": False, "message": "User with such email already exists"}

CREATE_ORDER_SUCCESS = {"success": True}
CREATE_ORDER_UNAUTHORIZED = {"success": False, "message": "You should be authorised"}
CREATE_ORDER_NO_INGREDIENTS = {"success": False, "message": "Ingredient ids must be provided"}

GET_ORDERS_SUCCESS = {"success": True}
GET_ORDERS_UNAUTHORIZED = {"success": False, "message": "You should be authorised"}

