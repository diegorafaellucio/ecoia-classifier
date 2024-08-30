from datetime import datetime, timedelta
from src.enum.configuration_enum import ConfigurationEnum
from src.controller.configuration_storage_controller import ConfigurationStorageController


class DateUtils:
    # logger = logging.getLogger(__name__)

    @staticmethod
    def get_start_interval_from_created_at():
        date = datetime.now()

        date = DateUtils.subtract_days(date, 1)

        date = DateUtils.reset_hour(date, [0, 0, 0])

        slaughter_start_hour = ConfigurationStorageController.get_config_data_value(ConfigurationEnum.SLAUGHTER_START_HOUR.key)

        new_date = DateUtils.add_hours(date, slaughter_start_hour)

        return new_date


    @staticmethod
    def get_finish_interval_from_created_at():
        date = datetime.now()

        date = DateUtils.subtract_days(date, 1)

        date = DateUtils.reset_hour(date, [23, 59, 59])

        slaughter_finish_hour = ConfigurationStorageController.get_config_data_value(
            ConfigurationEnum.SLAUGHTER_START_HOUR.key)

        new_date = DateUtils.add_hours(date, slaughter_finish_hour)

        return new_date

    @staticmethod
    def reset_hour(date, new_hour_data):
        return datetime(date.year, date.month, date.day, new_hour_data[0], new_hour_data[1], new_hour_data[2])

    @staticmethod
    def add_hours(date, hours):
        new_date = date + timedelta(hours=hours)
        return new_date

    @staticmethod
    def subtract_hours(date, hours):
        new_date = date - timedelta(hours=hours)
        return new_date

    @staticmethod
    def add_days(date, days):
        new_date = date + timedelta(days=days)
        return new_date

    @staticmethod
    def subtract_days(date, days):
        new_date = date - timedelta(days=days)
        return new_date



