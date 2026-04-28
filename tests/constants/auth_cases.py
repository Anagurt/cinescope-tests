from constants import CommonConstants
from resources.user_creds import RegularUserCreds, SuperAdminCreds

LOGIN_EXIST_USERS_CASES = [
    (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD),
    (RegularUserCreds.USERNAME, RegularUserCreds.PASSWORD),
]
LOGIN_EXIST_USERS_IDS = [
    "Авторизация супер-админа",
    "Авторизация пользователя",
]

REGISTER_EMPTY_FIELDS_CASES = [
    (
        CommonConstants.EMPTY_STR,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_VALID,
        CommonConstants.PASSWORD_VALID,
    ),
    (
        CommonConstants.EMAIL_VALID,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.EMPTY_STR,
        CommonConstants.PASSWORD_VALID,
    ),
    (
        CommonConstants.EMAIL_VALID,
        CommonConstants.EMPTY_STR,
        CommonConstants.PASSWORD_VALID,
        CommonConstants.PASSWORD_VALID,
    ),
    (
        CommonConstants.EMAIL_VALID,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_VALID,
        CommonConstants.EMPTY_STR,
    ),
]

REGISTER_EMPTY_FIELDS_IDS = [
    "Пустой email",
    "Пустой password",
    "Пустой full_name",
    "Пустой password_repeat",
]

REGISTER_ALREADY_EXISTS_CASES = [
    (
        SuperAdminCreds.USERNAME,
        CommonConstants.FULL_NAME_DEFAULT,
        SuperAdminCreds.PASSWORD,
        SuperAdminCreds.PASSWORD,
    ),
    (
        RegularUserCreds.USERNAME,
        CommonConstants.FULL_NAME_DEFAULT,
        RegularUserCreds.PASSWORD,
        RegularUserCreds.PASSWORD,
    ),
]

REGISTER_ALREADY_EXISTS_IDS = [
    "Регистрация уже существующего супер-админа",
    "Регистрация уже существующего пользователя",
]

REGISTER_INVALID_FIELDS_CASES = [
    (
        CommonConstants.INVALID_EMAIL_WITHOUT_AT,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_VALID,
        CommonConstants.PASSWORD_VALID,
    ),
    (
        CommonConstants.INVALID_EMAIL_DOMAIN_NO_DOT,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_VALID,
        CommonConstants.PASSWORD_VALID,
    ),
    (
        CommonConstants.INVALID_EMAIL_EMPTY_LOCAL,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_VALID,
        CommonConstants.PASSWORD_VALID,
    ),
    (
        CommonConstants.EMAIL_VALID,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_SHORT,
        CommonConstants.PASSWORD_SHORT,
    ),
    (
        CommonConstants.EMAIL_VALID,
        CommonConstants.FULL_NAME_DEFAULT,
        CommonConstants.PASSWORD_LONG,
        CommonConstants.PASSWORD_LONG,
    ),
]

REGISTER_INVALID_FIELDS_IDS = [
    "email без символа @",
    "email без точки",
    "email без локальной части",
    "слишком короткий password",
    "слишком длинный password",
]

LOGIN_EMPTY_FIELDS_CASES = [
    (CommonConstants.EMPTY_STR, RegularUserCreds.PASSWORD),
    (RegularUserCreds.USERNAME, CommonConstants.EMPTY_STR),
]

LOGIN_EMPTY_FIELDS_IDS = [
    "Пустой email",
    "Пустой password",
]

INVALID_USER_LOCATOR_CASES = [
    CommonConstants.NON_EXISTENT_ID,
    CommonConstants.NON_EXISTENT_EMAIL,
]
INVALID_USER_LOCATOR_IDS = [
    "Получение информации по ID",
    "Получение информации по Email",
]

REGULAR_USER_LOCATOR_CASES = [
    RegularUserCreds.ID,
    RegularUserCreds.USERNAME
]
REGULAR_USER_LOCATOR_IDS = [
    "Получение информации о пользователе по ID",
    "Получение информации о пользователе по Email",
]
