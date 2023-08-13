from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    h_to_m: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    calories_mean_speed_shift: float = 1.79
    calories_mean_speed_multiplier: int = 18
    h_to_m: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.distance = Training.get_distance(self)
        self.speed = Training.get_mean_speed(self)
        self.calories = Running.get_spent_calories(self)

    def get_spent_calories(self) -> float:

        return ((self.calories_mean_speed_multiplier * self.get_mean_speed()
                 + self.calories_mean_speed_shift) * self.weight / self.M_IN_KM
                * (self.duration * self.h_to_m))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cof_one = 0.035
    cof_two = 0.029
    kmh_to_ms = 0.278
    sm_to_m = 100
    h_to_m = 60

    def __init__(self, action: int, duration: float,
                 weight: float, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = Training.get_distance(self)
        self.speed = Training.get_mean_speed(self)
        self.calories = SportsWalking.get_spent_calories(self)

    def get_spent_calories(self) -> float:
        return ((self.cof_one * self.weight
                 + ((self.speed * self.kmh_to_ms)**2
                    / (self.height / self.sm_to_m))
                 * self.cof_two * self.weight) * self.h_to_m * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 1.38
    coef_one: float = 1.1
    coef_two: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = Training.get_distance(self)
        self.speed = Swimming.get_mean_speed(self)
        self.calories = Swimming.get_spent_calories(self)

    def get_spent_calories(self) -> float:
        return ((self.speed + self.coef_one) * self.coef_two
                * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    codes: dict = {'SWM': Swimming,
                   'RUN': Running,
                   'WLK': SportsWalking}
    return codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
