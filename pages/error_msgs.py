class ErrorMessages():
    ERROR_Q_MUST_BE_GE_THAN_3 = "Параметр 'q' должен быть не менее 3 символов"
    ERROR_Q_MUST_BE_LE_THAN_30 = "Параметр 'q' должен быть не более 30 символов"
    ERROR_PAGE_MUST_BE_G_THAN_0 = "Параметр 'page' должен быть больше 0"
    ERROR_PAGE_MUST_BE_NATURAL_NUMBER = "Параметр 'page' должен быть целым числом"
    ERROR_INVALID_COUNTRY_CODE = "Параметр 'country_code' может быть одним из следующих значений: ru, kg, kz, cz"
    ERROR_PAGE_SIZE_CAN_BE = "Параметр 'page_size' может быть одним из следующих значений: 5, 10, 15"
    ERROR_PAGE_SIZE_CAN_BE_A_NUMBER = "Параметр 'page_size' должен быть целым числом"


class CountryCount():
    RU = 13
    KZ = 4
    KG = 3
    CZ = 1