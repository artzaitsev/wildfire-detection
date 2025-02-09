from internal.services.weather.fwi_indices import ffmc, dmc, dc, isi, bui, fwi

class FireWeatherIndex:
    def __init__(
        self,
        temp: float,
        rh: float,
        ws: float,
        prec: float,
        lat: float,
        mon: int,
        ffmc_yda: float = 85.0,
        dmc_yda: float = 6.0,
        dc_yda: float = 15.0,
        lat_adjust: bool = True,
    ):
        """
        Класс-обёртка для вычисления индексов лесных пожаров на основе погодных данных.

        :param temp: Температура (°C)
        :param rh: Влажность воздуха (%)
        :param ws: Скорость ветра (км/ч)
        :param prec: Осадки (мм)
        :param lat: Широта местности (°)
        :param mon: Номер месяца (1-12)
        :param ffmc_yda: Значение FFMC с предыдущего дня (0-101) (по умолчанию 85.0)
        :param dmc_yda: Значение DMC с предыдущего дня (≥ 0) (по умолчанию 6.0)
        :param dc_yda: Значение DC с предыдущего дня (≥ 0) (по умолчанию 15.0)
        :param lat_adjust: Нужно ли учитывать широту при расчётах (по умолчанию `True`)
        """
        self.temp: float = temp
        self.rh: float = rh
        self.ws: float = ws
        self.prec: float = prec
        self.lat: float = lat
        self.mon: int = mon
        self.ffmc_yda: float = ffmc_yda
        self.dmc_yda: float = dmc_yda
        self.dc_yda: float = dc_yda
        self.lat_adjust: bool = lat_adjust

    def get_ffmc(self) -> float:
        """Вычисляет Fine Fuel Moisture Code (FFMC)."""
        return ffmc(self.ffmc_yda, self.temp, self.rh, self.ws, self.prec)

    def get_dmc(self) -> float:
        """Вычисляет Duff Moisture Code (DMC)."""
        return dmc(self.dmc_yda, self.temp, self.rh, self.prec, self.lat, self.mon, self.lat_adjust)

    def get_dc(self) -> float:
        """Вычисляет Drought Code (DC)."""
        return dc(self.dc_yda, self.temp, self.rh, self.prec, self.lat, self.mon, self.lat_adjust)

    def get_isi(self) -> float:
        """Вычисляет Initial Spread Index (ISI)."""
        ffmc_value: float = self.get_ffmc()
        return isi(ffmc_value, self.ws)

    def get_bui(self) -> float:
        """Вычисляет Buildup Index (BUI)."""
        dmc_value: float = self.get_dmc()
        dc_value: float = self.get_dc()
        return bui(dmc_value, dc_value)

    def get_fwi(self) -> float:
        """Вычисляет Fire Weather Index (FWI)."""
        isi_value: float = self.get_isi()
        bui_value: float = self.get_bui()
        return fwi(isi_value, bui_value)
