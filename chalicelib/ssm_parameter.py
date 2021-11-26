from chalicelib.config import Config
import boto3

ssm = boto3.client('ssm')

class SSMParameter:
    def get() -> str:
        parameter = ssm.get_parameter(Name=Config.SSM_PARAMETER_LAST_POMODORO)
        return parameter['Parameter']['Value']

    def save(value:str) -> None:
        parameter = ssm.put_parameter(Name=Config.SSM_PARAMETER_LAST_POMODORO,
                                      Value=str(value),
                                      Overwrite=True
        )
        return parameter
