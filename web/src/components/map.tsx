import { useEffect, useRef, useState } from "react";
import { Input } from "@heroui/input";
import {Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, useDisclosure} from "@heroui/modal"
import {Card, CardBody } from "@heroui/card";
import clsx from "clsx";
import LatLngBounds = google.maps.LatLngBounds;

const API_KEY = "AIzaSyC5m7jGq5n-FCu0ZPAhg_XVZ_JBpevOFUU"; // 🔥 Замените на свой API-ключ

declare global {
  interface Window {
    google: typeof google;
  }
}

// https://www.svgrepo.com/collection/emoji-6/
export const SmileVector = (props: any) => {
  return (
      <svg height="5em" width="5em" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
           xmlns:xlink="http://www.w3.org/1999/xlink"
           viewBox="0 0 512.003 512.003" xml:space="preserve"
          {...props}
      >
      <circle style={{ fill:'#FDDF6D' }} cx="256.001" cy="256.001" r="256.001"/>
              <path style={{fill: '#FCC56B'}} d="M310.859,474.208c-141.385,0-256-114.615-256-256c0-75.537,32.722-143.422,84.757-190.281
          C56.738,70.303,0,156.525,0,256c0,141.385,114.615,256,256,256c65.849,0,125.883-24.87,171.243-65.718
          C392.325,464.135,352.77,474.208,310.859,474.208z"/>
              <g>
          <path style={{fill:'#7F184C'}} d="M293.248,427.894L293.248,427.894c-57.23,0-103.624-46.394-103.624-103.624l0,0h207.248l0,0
              C396.872,381.5,350.477,427.894,293.248,427.894z"/>
                <path style={{ fill: '#7F184C'}} d="M245.899,187.173c-5.752,0-10.414-4.663-10.414-10.414c0-13.433-10.928-24.362-24.362-24.362
              c-13.433,0-24.362,10.93-24.362,24.362c0,5.752-4.663,10.414-10.414,10.414c-5.752,0-10.414-4.663-10.414-10.414
              c0-24.918,20.273-45.19,45.19-45.19s45.19,20.272,45.19,45.19C256.314,182.51,251.651,187.173,245.899,187.173z"/>
                <path style={{fill:'#7F184C'}} d="M421.798,187.173c-5.752,0-10.414-4.663-10.414-10.414c0-13.433-10.928-24.362-24.362-24.362
              s-24.362,10.93-24.362,24.362c0,5.752-4.663,10.414-10.414,10.414s-10.414-4.663-10.414-10.414c0-24.918,20.273-45.19,45.19-45.19
              s45.19,20.272,45.19,45.19C432.213,182.51,427.55,187.173,421.798,187.173z"/>
      </g>
              <g>
          <path style={{fill:'#F9A880'}} d="M145.987,240.152c-19.011,0-34.423,15.412-34.423,34.423h68.848
              C180.41,255.564,164.998,240.152,145.987,240.152z"/>
                <path style={{fill:'#F9A880'}} d="M446.251,235.539c-19.011,0-34.423,15.412-34.423,34.423h68.848
              C480.676,250.951,465.264,235.539,446.251,235.539z"/>
      </g>
              <path style={{ fill:'#F2F2F2' }} d="M214.907,324.27v16.176c0,6.821,5.529,12.349,12.349,12.349h131.982
          c6.821,0,12.349-5.529,12.349-12.349V324.27H214.907z"/>
              <path style={{fill:'#FC4C59'}} d="M295.422,384.903c-28.011-13.014-59.094-11.123-84.3,2.374c18.94,24.686,48.726,40.616,82.245,40.616
          l0,0c14.772,0,28.809-3.112,41.526-8.682C325.564,404.777,312.187,392.692,295.422,384.903z"/>
              <ellipse transform="matrix(0.2723 -0.9622 0.9622 0.2723 151.7762 343.0422)" style={{fill:'#FCEB88'}} cx="302.685"
                       cy="71.177" rx="29.854" ry="53.46"/>
      </svg>
  )
}

export const NeutralSmileVector = (props: any) => {
  return (
      <svg height="5em" width="5em" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
           xmlns:xlink="http://www.w3.org/1999/xlink"
           viewBox="0 0 512.003 512.003" xml:space="preserve"
          {...props}
      >
      <circle style={{ fill:'#FDDF6D' }} cx="256.001" cy="256.001" r="256.001"/>
              <path style={{fill: '#FCC56B'}} d="M310.859,474.208c-141.385,0-256-114.615-256-256c0-75.537,32.722-143.422,84.757-190.281
          C56.738,70.303,0,156.525,0,256c0,141.385,114.615,256,256,256c65.849,0,125.883-24.87,171.243-65.718
          C392.325,464.135,352.77,474.208,310.859,474.208z"/>
              <g>
          <circle style={{fill:'#7F184C'}} cx="211.414" cy="176.754" r="31.243"/>
                <circle style={{ fill: '#7F184C'}} cx="387.321" cy="176.754" r="31.243"/>
      </g>
              <g>
          <path style={{fill:'#F9A880'}} d="M145.987,240.152c-19.011,0-34.425,15.412-34.425,34.425h68.848
              C180.41,255.564,164.998,240.152,145.987,240.152z"/>
                <path style={{fill:'#F9A880'}} d="M446.251,235.539c-19.011,0-34.425,15.412-34.425,34.425h68.848
              C480.676,250.951,465.264,235.539,446.251,235.539z"/>
      </g>
              <path style={{fill:'#7F184C'}} d="M401.566,359.206H213.621c-5.753,0-10.414-4.663-10.414-10.414s4.662-10.414,10.414-10.414h187.945
          c5.753,0,10.414,4.663,10.414,10.414S407.319,359.206,401.566,359.206z"/>
              <ellipse transform="matrix(0.2723 -0.9622 0.9622 0.2723 136.205 334.8704)" style={{fill:'#FCEB88'}} cx="289.497"
                       cy="77.385" rx="29.854" ry="53.46"/>
      </svg>
  )
}

// export const ScarySmileVector = (props: any) => {
//     return (
//         <svg height="800px" width="800px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
//              xmlns:xlink="http://www.w3.org/1999/xlink"
//              viewBox="0 0 512.003 512.003" xml:space="preserve">
//         <circle style="fill:#FDDF6D;" cx="256.001" cy="256.001" r="256.001"/>
//                     <path style="fill:#FCC56B;" d="M310.859,474.208c-141.385,0-256-114.615-256-256c0-75.537,32.722-143.422,84.757-190.281
//             C56.738,70.303,0,156.525,0,256c0,141.385,114.615,256,256,256c65.849,0,125.883-24.87,171.243-65.718
//             C392.325,464.135,352.77,474.208,310.859,474.208z"/>
//                     <g>
//             <circle style="fill:#FFFFFF;" cx="211.414" cy="176.754" r="57.836"/>
//                         <circle style="fill:#FFFFFF;" cx="419.675" cy="176.754" r="74.262"/>
//         </g>
//                     <g>
//             <path style="fill:#F9A880;" d="M145.987,279.188c-19.011,0-34.423,15.412-34.423,34.425h68.848
//                 C180.41,294.6,164.998,279.188,145.987,279.188z"/>
//                         <path style="fill:#F9A880;" d="M446.251,274.575c-19.011,0-34.423,15.412-34.423,34.425h68.848
//                 C480.676,289.987,465.264,274.575,446.251,274.575z"/>
//         </g>
//                     <g>
//             <circle style="fill:#7F184C;" cx="221.148" cy="176.754" r="20.829"/>
//                         <circle style="fill:#7F184C;" cx="435.241" cy="176.754" r="20.829"/>
//                         <path style="fill:#7F184C;" d="M313.382,321.154L313.382,321.154c43.882,0,79.457,35.574,79.457,79.457v24.167H233.926v-24.167
//                 C233.926,356.727,269.5,321.154,313.382,321.154z"/>
//         </g>
//                     <path style="fill:#F2F2F2;" d="M265.683,349.679h101.201c2.047,0,3.937-0.855,5.485-2.294
//             c-14.541-16.105-35.58-26.231-58.986-26.231l0,0c-21.693,0-41.345,8.702-55.684,22.795
//             C259.38,347.389,262.324,349.679,265.683,349.679z"/>
//                     <path style="fill:#FC4C59;" d="M301.982,395.466c-21.565-13.067-44.685-16.295-66.382-11.121c-1.093,5.25-1.672,10.689-1.672,16.265
//             v24.167H333.99C324.999,412.924,314.267,402.911,301.982,395.466z"/>
//                     <ellipse transform="matrix(0.2723 -0.9622 0.9622 0.2723 139.1086 326.3136)" style="fill:#FCEB88;"
//                              cx="285.292" cy="71.187" rx="29.854" ry="53.46"/>
//         </svg>
//     )
// }

export const LocationIcon = (props: any) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" height="1.2em" viewBox="0 0 24 24" width="1.2em"
             fill="#5f6368" {...props}>
            <path d="M0 0h24v24H0z" fill="none"/>
            <path
                d="M12 12c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm6-1.8C18 6.57 15.35 4 12 4s-6 2.57-6 6.2c0 2.34 1.95 5.44 6 9.14 4.05-3.7 6-6.8 6-9.14zM12 2c4.2 0 8 3.22 8 8.2 0 3.32-2.67 7.25-8 11.8-5.33-4.55-8-8.48-8-11.8C4 5.22 7.8 2 12 2z"/>
        </svg>
    )
}

export const SearchIcon = (props: any) => {
    return (
        <svg
            aria-hidden="true"
            fill="none"
            focusable="false"
            height="1em"
            role="presentation"
            viewBox="0 0 24 24"
            width="1em"
            {...props}
        >
            <path
                d="M11.5 21C16.7467 21 21 16.7467 21 11.5C21 6.25329 16.7467 2 11.5 2C6.25329 2 2 6.25329 2 11.5C2 16.7467 6.25329 21 11.5 21Z"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
            />
            <path
                d="M22 22L20 20"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
            />
        </svg>
    );
};

const GoogleMap = () => {
    const mapContainer = useRef<any>(null);
    const mapRef = useRef<any>(null);
    const markerRef = useRef<any>(null);
    const clickTimeoutRef = useRef<any>(null);
    const isDoubleClickRef = useRef(false)

    const [coordinates, setCoordinates] = useState({lat: 55.751574, lng: 37.573856});
    const [place, setPlace] = useState("");
    const {isOpen, onOpen, onOpenChange} = useDisclosure();
    const [value, setValue] = useState('')
    const geocoderRef = useRef<any>(null);

    useEffect(() => {
        const loadGoogleMaps = async () => {
            if (!window.google) {
        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places,maps`;
        script.async = true;
        script.onload = initMap;
        document.head.appendChild(script);
      } else {
        initMap();
      }
    };

    const initMap = () => {
      if (!mapContainer.current) return;

      const map = new google.maps.Map(mapContainer.current, {
        center: coordinates,
        zoom: 10,
        mapTypeId: "roadmap",
      });

      mapRef.current = map;
      geocoderRef.current = new google.maps.Geocoder();

      const input = document.getElementById("search-box") as HTMLInputElement;
      const searchBox = new google.maps.places.SearchBox(input);

      map.addListener("bounds_changed", () => {
        searchBox.setBounds(map.getBounds() as LatLngBounds);
      });

      searchBox.addListener("places_changed", () => {
        const places = searchBox.getPlaces();
        if (!places || places.length === 0) return;

        const place = places[0];
        const location = place.geometry?.location;
        if (!location) return;

        setCoordinates({ lat: location.lat(), lng: location.lng() });
        setPlace(place.formatted_address || place.name || '')
        setValue(place.formatted_address || place.name || '')
        map.setCenter(location);
        placeMarker(location);

        setTimeout(() => {
          onOpen()
        }, 300)
      });

      map.addListener("click", (event: { latLng: any; }) => {
        clickTimeoutRef.current = setTimeout(() => {
          if (isDoubleClickRef.current) {
            return; // Если это двойной клик — выходим
          }

          const clickedLocation = event.latLng;
          setCoordinates({ lat: clickedLocation.lat(), lng: clickedLocation.lng() });
          placeMarker(clickedLocation);
          onOpen();

          // Получаем адрес по координатам
          if (geocoderRef.current) {
            geocoderRef.current.geocode({ location: clickedLocation }, (results: any[], status: string) => {
              if (status === "OK" && results[0]) {
                setValue(results[0].formatted_address);
                setPlace(results[0].formatted_address)
              }
            });
          }
        }, 300); // Сбросим флаг через 300 мс
      });

      map.addListener("dblclick", () => {
        isDoubleClickRef.current = true;
        clearTimeout(clickTimeoutRef.current);
        setTimeout(() => {
          isDoubleClickRef.current = false;
        }, 400); // Сбросим флаг через 300 мс
      });
    };

    const placeMarker = (location: any) => {
      if (markerRef.current) {
        markerRef.current.setMap(null);
      }

      const marker = new google.maps.Marker({
        position: location,
        map: mapRef.current,
      });
      markerRef.current = marker;
    };

    loadGoogleMaps();
  }, []);

  // const [fireRisk, setFireRisk] = useState(0)
  const [fireRisk] = useState(2)

  return (
    <div>
      <div className="max-w-3xl mx-auto px-5 pb-10">
        <Input
            isClearable
            id="search-box"
            label="Search"
            placeholder="Type region, city or coordinates..."
            startContent={
              <SearchIcon className="text-black/50 mb-0.5 dark:text-white/90 text-slate-400 pointer-events-none flex-shrink-0" />
            }
            value={value} onValueChange={setValue}
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
                    <LocationIcon style={{display: 'inline-block', paddingBottom: '2px'}}/>
                    {coordinates.lat.toFixed(4)},{coordinates.lng.toFixed(4)}
                  </small>
                  <h4 className="font-bold text-large">{place}</h4>
                    </div>
                </ModalHeader>
                <ModalBody>
                  <Card
                    className={
                      clsx({
                        "bg-green-300": fireRisk === 0,
                        "bg-yellow-100": fireRisk === 1
                      })
                    }
                    shadow="none"
                  >
                    <CardBody className="overflow-visible py-2 text-center">
                      {/*<p className="text-2xl py-8"><SmileVector style={{ display: 'inline-block' }}/></p>*/}
                      <p className="text-2xl py-8">
                        {
                          fireRisk === 0? (
                            <SmileVector style={{ display: 'inline-block' }}/>
                          ) : fireRisk === 1? (
                            <NeutralSmileVector style={{ display: 'inline-block' }}/>
                          ) : (
                            "High risk of fire"
                          )
                        }
                      </p>
                      <p className="text-xl uppercase pb-4 font-bold">
                        {
                          fireRisk === 0? "Low fire risk" : fireRisk === 1? "Medium fire risk" : "High fire risk"
                        }
                      </p>
                    </CardBody>
                  </Card>
                </ModalBody>

                <ModalFooter>
                  {/*<Button color="danger" variant="light" onPress={onClose}>*/}
                  {/*  Close*/}
                  {/*</Button>*/}
                  {/*<Button color="primary" onPress={onClose}>*/}
                  {/*  Action*/}
                  {/*</Button>*/}
                </ModalFooter>
              </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

export default GoogleMap;