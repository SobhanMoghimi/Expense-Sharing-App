from rest_framework import status
from rest_framework.response import Response

from esa.app.api.serializer.system.system_serializer import ResponseSerializer
from esa.app.models.vo.response_vo import ResponseVO


class SuccessfulResponse(Response):
    def __init__(self):
        self.default_message = ResponseVO.successful
        self.default_status = status.HTTP_200_OK
        response = ResponseSerializer(
            {ResponseVO.message: self.default_message, ResponseVO.status_code: self.default_status})
        super().__init__(data=response.data,
                         status=self.default_status)


class CreateResponse(Response):
    def __init__(self):
        self.default_message = "create_successfully"
        self.default_status = status.HTTP_201_CREATED
        response = ResponseSerializer(
            {ResponseVO.message: self.default_message, ResponseVO.status_code: self.default_status})
        super().__init__(data=response.data,
                         status=self.default_status)


class UpdateResponse(Response):
    def __init__(self):
        self.default_message = ResponseVO.update_successfully
        self.default_status = status.HTTP_201_CREATED
        response = ResponseSerializer(
            {ResponseVO.message: self.default_message, ResponseVO.status_code: self.default_status})
        super().__init__(data=response.data,
                         status=self.default_status)


class DeleteResponse(Response):
    def __init__(self):
        self.default_message = ResponseVO.delete_successfully
        self.default_status = status.HTTP_200_OK
        response = ResponseSerializer(
            {ResponseVO.message: self.default_message, ResponseVO.status_code: self.default_status})
        super().__init__(data=response.data,
                         status=self.default_status)


class ErrorResponse(Response):
    def __init__(self, status_code: int, message=None):
        if message is None:
            self.error = ResponseSerializer(
                {ResponseVO.message: ResponseVO.invalid_input, ResponseVO.status_code: status_code})
        else:
            self.error = ResponseSerializer(
                {ResponseVO.message: str(message), ResponseVO.status_code: status_code})

        super().__init__(data=self.error.data, status=status_code)