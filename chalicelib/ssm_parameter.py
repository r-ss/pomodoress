from chalicelib.config import Config
import os
import boto3

ssm = boto3.client('ssm')

class SSMParameter:
    def get() -> str:
        if not Config.AWS_SSM_ENABLED:
            if Config.SSM_PARAMETER_LAST_POMODORO in os.environ:
                return os.environ.get(Config.SSM_PARAMETER_LAST_POMODORO)
            return 'dummy'
        parameter = ssm.get_parameter(Name=Config.SSM_PARAMETER_LAST_POMODORO)
        return parameter['Parameter']['Value']

    def save(value:str) -> None:
        if not Config.AWS_SSM_ENABLED:
            os.environ[Config.SSM_PARAMETER_LAST_POMODORO] = str(value)
            return None
        parameter = ssm.put_parameter(Name=Config.SSM_PARAMETER_LAST_POMODORO,
                                      Value=str(value),
                                      Overwrite=True)
        return parameter
