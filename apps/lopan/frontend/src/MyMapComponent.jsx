import { MapContainer, TileLayer, Marker, Polyline, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { useEffect } from 'react';

// 地図の中心を自動更新する補助コンポーネント
function ChangeView({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center);
  }, [center, map]);
  return null;
}

const MyMapComponent = ({ center, angle }) => {
  // アイコンの設定
  const icon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41]
  });

  // 羅盤の方位角（angle）に合わせてレーザー線の終点を計算
  const length = 0.01; 
  const endPoint = [
    center.lat + length * Math.cos((angle - 90) * (Math.PI / 180)),
    center.lng + length * Math.sin((angle - 90) * (Math.PI / 180))
  ];

  return (
    <MapContainer 
      center={center} 
      zoom={15} 
      style={{ height: '100%', width: '100%' }} 
      zoomControl={false}
    >
      <ChangeView center={center} />
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <Marker position={center} icon={icon} />
      {/* 方位を示すレーザー線 */}
      <Polyline positions={[ [center.lat, center.lng], endPoint ]} color="red" weight={3} />
    </MapContainer>
  );
};

export default MyMapComponent;