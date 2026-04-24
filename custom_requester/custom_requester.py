import json
import logging
import os
import re
from http import HTTPStatus

import requests
from pydantic import BaseModel

from constants import GREEN, RED, RESET


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, session: requests.Session, base_url: str) -> None:
        """
        Инициализация кастомного реквестера.
        :param session: Объект requests.Session.
        :param base_url: Базовый URL API.
        """
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        expected_status: HTTPStatus | None = HTTPStatus.OK,
        need_logging: bool = True,
        response_model: type[BaseModel] | None = None,
        attach_error_messages: bool = False,
        allure_attachment_name: str = "Сообщения об ошибках API",
        success_response_model: type[BaseModel] | None = None,
        error_response_model: type[BaseModel] | None = None,
    ) -> requests.Response:
        """
        Универсальный метод для отправки запросов.
        :param method: HTTP метод (GET, POST, PUT, DELETE и т.д.).
        :param endpoint: Эндпоинт (например, "/login").
        :param data: Тело запроса (JSON-данные).
        :param expected_status: Ожидаемый статус-код (по умолчанию 200).
            Если None — проверка не выполняется.
        :param need_logging: Флаг для логирования (по умолчанию True).
        :param response_model: Pydantic-модель для валидации JSON-ответа.
        :param attach_error_messages: Прикрепить поле message в Allure.
        :param allure_attachment_name: Название вложения в Allure.
        :param success_response_model: Pydantic-модель для валидации успешного ответа.
        :param error_response_model: Pydantic-модель для валидации ошибочного ответа.
        :return: Объект ответа requests.Response.
        """
        url = f"{self.base_url}{endpoint}"
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))
        response = self.session.request(method,
                                        url,
                                        json=data,
                                        headers=self.headers,
                                        params=params)
        if need_logging:
            self.log_request_and_response(response)

        if (expected_status is not None
                and response.status_code != expected_status):
            raise ValueError(
                f"Unexpected status code: {response.status_code}. "
                f"Expected: {expected_status}"
            )
        validated_response = None
        if response_model is not None:
            success_response_model = success_response_model or response_model
            error_response_model = error_response_model or response_model
            
        model_to_validate = None
        if 200 <= response.status_code < 300:
            model_to_validate = success_response_model
        elif 400 <= response.status_code < 600:
            model_to_validate = error_response_model

        if model_to_validate is not None:
            validated_response = model_to_validate.model_validate(response.json())
            setattr(response, "validated_response", validated_response)

        if attach_error_messages:
            self._attach_error_messages(
                response=response,
                validated_response=validated_response,
                attachment_name=allure_attachment_name,
            )

        return response

    @staticmethod
    def _extract_pytest_case_id() -> str:
        current_test = os.environ.get("PYTEST_CURRENT_TEST", "")
        match = re.search(r"\[([^\]]+)\]", current_test)
        if match is None:
            return current_test.replace(" (call)", "")
        return match.group(1)

    def _attach_error_messages(
        self,
        response: requests.Response,
        validated_response: BaseModel | None = None,
        attachment_name: str = "Сообщения об ошибках API",
    ) -> None:
        try:
            import allure
        except ImportError:
            self.logger.warning("Allure не установлен, attachment пропущен")
            return

        message_value = None
        if validated_response is not None:
            message_value = getattr(validated_response, "message", None)

        if message_value is None:
            try:
                response_json = response.json()
                message_value = response_json.get("message")
            except ValueError:
                self.logger.warning("Ответ не JSON, attachment пропущен")
                return

        if message_value is None:
            self.logger.warning("В ответе отсутствует поле message для attachment")
            return

        messages = message_value if isinstance(message_value, list) else [message_value]
        case_id = self._extract_pytest_case_id()
        text = f"{case_id}\n\n" + "\n".join(f'"{message}"' for message in messages)
        allure.attach(
            text,
            name=attachment_name,
            attachment_type=allure.attachment_type.TEXT,
        )

    def _update_session_headers(self, **kwargs: str) -> None:
        """
        Обновление заголовков сессии.
        :param kwargs: Дополнительные заголовки.
        """
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def log_request_and_response(self, response: requests.Response) -> None:
        """
        Логирование запросов и ответов.
        :param response: Объект ответа requests.Response.
        """
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join([
                f"-H '{header}: {value}'"
                for header, value in request.headers.items()
            ])
            current_test = os.environ.get("PYTEST_CURRENT_TEST", "").replace(
                " (call)", "")
            full_test_name = f"pytest {current_test}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            # Логируем запрос
            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(f"{GREEN}{full_test_name}{RESET}\n"
                             f"curl -X {request.method} '{request.url}' \\\n"
                             f"{headers} \\\n"
                             f"{body}")

            # Обрабатываем ответ
            response_status = response.status_code
            is_success = response.ok
            response_data = response.text

            # Попытка форматировать JSON
            try:
                response_data = json.dumps(json.loads(response.text),
                                           indent=4,
                                           ensure_ascii=False)
            except json.JSONDecodeError:
                pass  # Оставляем текст, если это не JSON

            # Логируем ответ
            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not is_success:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response_status}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}")
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}\n"
                    f"\tDATA:\n{response_data}")
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")
