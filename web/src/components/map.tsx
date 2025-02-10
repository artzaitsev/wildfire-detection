import LatLngBounds = google.maps.LatLngBounds;

import {useEffect, useRef, useState} from "react";
import {Input} from "@heroui/input";
import {Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, useDisclosure,} from "@heroui/modal";
import {Card, CardBody} from "@heroui/card";
import clsx from "clsx";
import {LocationIcon, NeutralSmileVector, ScarySmileVector, SearchIcon, SmileVector} from "@/components/icons.tsx";

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

declare global {
  interface Window {
    google: typeof google;
  }
}

const GoogleMap = () => {
  const mapContainer = useRef<any>(null);
  const mapRef = useRef<any>(null);
  const markerRef = useRef<any>(null);
  const clickTimeoutRef = useRef<any>(null);
  const isDoubleClickRef = useRef(false);

  const [coordinates, setCoordinates] = useState({
    lat: 55.751574,
    lng: 37.573856,
  });
  const [place, setPlace] = useState("");
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [value, setValue] = useState("");
  const geocoderRef = useRef<any>(null);

  useEffect(() => {
    // Функция для загрузки скрипта Google Maps API, если он ещё не загружен
    const loadGoogleMaps = async () => {
      if (!window.google) {
        // Создаём новый элемент script для подключения API
        const script = document.createElement("script");

        script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places,maps`;
        script.async = true;
        script.onload = initMap;
        document.head.appendChild(script);
      } else {
        // Если библиотека уже загружена, сразу инициализируем карту
        initMap();
      }
    };

    // Инициализации карты
    const initMap = () => {
      // Проверяем, существует ли контейнер для карты
      if (!mapContainer.current) return;

      // Создаём объект карты с нужными параметрами
      const map = new google.maps.Map(mapContainer.current, {
        center: coordinates,  // Начальные координаты центра карты, дефолтные - Москва
        zoom: 10,              // Начальный уровень масштабирования
        mapTypeId: "roadmap",  // Тип карты (дорожная карта)
      });

      mapRef.current = map; // Сохраняем реф на карту для дальнейшего использования
      geocoderRef.current = new google.maps.Geocoder(); // Инициализируем геокодер, чтобы отобразить название локации при ручном выборе на карте

      // Получаем элемент input для поиска по адресу
      const input = document.getElementById("search-box") as HTMLInputElement;
      // Инициализируем саджест адресов google
      const searchBox = new google.maps.places.SearchBox(input);

      // Устанавливаем границы поисковой области по измененным границам карты (улучшает качество поиска)
      map.addListener("bounds_changed", () => {
        searchBox.setBounds(map.getBounds() as LatLngBounds);
      });

      // Обработчик событий выбора локации в searchbox
      searchBox.addListener("places_changed", () => {
        const places = searchBox.getPlaces();

        if (!places || places.length === 0) return;

        const place = places[0];
        const location = place.geometry?.location;

        if (!location) return;

        // Обновляем координаты и адрес выбранного места
        setCoordinates({ lat: location.lat(), lng: location.lng() });
        setPlace(place.formatted_address || place.name || "");
        setValue(place.formatted_address || place.name || "");
        map.setCenter(location);
        placeMarker(location);

        // Открываем с небольшой задержкой попап статуса пожара
        setTimeout(() => {
          onOpen();
        }, 300);
      });

      // Обработчик события клика по карте для выставления маркера и определения места
      map.addListener("click", (event: { latLng: any }) => {
        clickTimeoutRef.current = setTimeout(() => {
          if (isDoubleClickRef.current) {
            return; // Если это двойной клик — выходим
          }

          const clickedLocation = event.latLng;

          // Обновляем координаты и размещаем маркер
          setCoordinates({
            lat: clickedLocation.lat(),
            lng: clickedLocation.lng(),
          });
          placeMarker(clickedLocation);
          onOpen();

          // Получаем адрес по координатам с помощью геокодера
          if (geocoderRef.current) {
            geocoderRef.current.geocode(
              { location: clickedLocation },
              (results: any[], status: string) => {
                if (status === "OK" && results[0]) {
                  setValue(results[0].formatted_address);
                  setPlace(results[0].formatted_address);
                }
              },
            );
          }
        }, 300); // Сбросим флаг через 300 мс
      });

      // Обработчик двойного клика, чтобы отличать размещение маркера и увеличения карты по двойному клику
      map.addListener("dblclick", () => {
        isDoubleClickRef.current = true;
        clearTimeout(clickTimeoutRef.current); // Очищаем предыдущую задержку
        setTimeout(() => {
          isDoubleClickRef.current = false;
        }, 400); // Сбросим флаг через 400 мс
      });
    };

    // Функция для размещения маркера на карте
    const placeMarker = (location: any) => {
      // Если маркер уже существует, удаляем его
      if (markerRef.current) {
        markerRef.current.setMap(null);
      }

      // Создаём новый маркер и добавляем его на карту
      markerRef.current = new google.maps.Marker({
        position: location,
        map: mapRef.current,
      });
    };

    loadGoogleMaps();
  }, []);

  const [fireRisk, setFireRisk] = useState(0);

  useEffect(() => {
    // Делаем запрос на бэк для получения прогноза по пожарам, используя текущие координаты
    (async function f() {
      try {
        if (!isOpen) {
          return;
        }
        const response = (await fetch(
          `/api/v1/wildfire/predict?lat=${coordinates.lat}3&lon=${coordinates.lng}`,
        ).then((res) => res.json())) as { data: number };

        // Высокий риск пожара
        if (response.data > 0.9) {
          return setFireRisk(2);
        }

        // Средний риск пожара
        if (response.data > 0.7) {
          return setFireRisk(1);
        }

        // Низкий риск пожара
        return setFireRisk(0);
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    })();
  }, [isOpen, coordinates]); // Хук будет перезапускаться при изменении значений isOpen или coordinates

  return (
    <div>
      <div className="max-w-3xl mx-auto px-5 pb-10">
        <Input
          isClearable
          id="search-box"
          label="Поиск"
          placeholder="Введите название места или коориднаты..."
          startContent={
            <SearchIcon className="text-black/50 mb-0.5 dark:text-white/90 text-slate-400 pointer-events-none flex-shrink-0" />
          }
          value={value}
          onValueChange={setValue}
        />
      </div>

      <div ref={mapContainer} style={{ width: "100%", height: "60vh" }} />

      <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent>
          {() => (
            <>
              <ModalHeader>
                <div className="flex-col items-start pb-5">
                  <small className="w-full pb-1 text-gray-500">
                    <LocationIcon
                      style={{ display: "inline-block", paddingBottom: "2px" }}
                    />
                    {coordinates.lat.toFixed(4)},{coordinates.lng.toFixed(4)}
                  </small>
                  <h4 className="font-bold text-large">{place}</h4>
                </div>
              </ModalHeader>
              <ModalBody>
                <Card
                  className={clsx({
                    "bg-green-300": fireRisk === 0,
                    "bg-yellow-100": fireRisk === 1,
                    "bg-red-400": fireRisk === 2,
                  })}
                  shadow="none"
                >
                  <CardBody className="overflow-visible py-2 text-center">
                    <p className="text-2xl py-8">
                      {fireRisk === 0 ? (
                        <SmileVector style={{ display: "inline-block" }} />
                      ) : fireRisk === 1 ? (
                        <NeutralSmileVector
                          style={{ display: "inline-block" }}
                        />
                      ) : (
                        <ScarySmileVector style={{ display: "inline-block" }} />
                      )}
                    </p>
                    <p className="text-xl uppercase pb-4 font-bold">
                      {fireRisk === 0
                        ? "Риск пожара низкий"
                        : fireRisk === 1
                          ? "Риск пожара средний"
                          : "Риск пожара высокий"}
                    </p>
                  </CardBody>
                </Card>
              </ModalBody>
              <ModalFooter className="pt-2 pb-6">
                {/*<Input*/}
                {/*  isClearable*/}
                {/*  id="search-box"*/}
                {/*  label="Поиск"*/}
                {/*  placeholder="Введите название места или коориднаты..."*/}
                {/*  startContent={*/}
                {/*    <SearchIcon className="text-black/50 mb-0.5 dark:text-white/90 text-slate-400 pointer-events-none flex-shrink-0" />*/}
                {/*  }*/}
                {/*  value={value}*/}
                {/*  onValueChange={setValue}*/}
                {/*/>*/}
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

export default GoogleMap;
