import { useEffect, useState } from "react";
import FuturePrayers from "./components/layout/FuturePrayers";
import Header from "./components/layout/Header";
import type { Prayer } from "./models/prayers.model";
import CurrentPrayer from "./components/layout/CurrentPrayer";

export default function App() {
  const lat = 42.6629,
    lng = 21.1655;

  const [prayers, setPrayers] = useState<Prayer[] | null>(null);
  useEffect(() => {
    const fetchPrayers = async () => {
      const res = await fetch(
        `http://127.0.0.1:8000/api/prayers?lat=${lat}&lng=${lng}`,
      );

      const data = (await res.json()) as Prayer[];
      console.log(data);
      setPrayers(data);
    };

    fetchPrayers();
  }, []);

  const getCurrentPrayer = () => {
    if (!prayers) return { name: "", time: "" };
    let currentPrayer: Prayer = { name: "", time: "" };
    const now = new Date();
    prayers.forEach((p) => {
      const time = new Date(p.time);
      if (now.getTime() > time.getTime()) {
        currentPrayer = p;
      } else {
        return;
      }
    });

    return currentPrayer;
  };

  const getNextPrayer = () => {
    if (!prayers) return { name: "", time: "" };
    const now = new Date();
    let timeLeft;
    const nextPrayer = prayers.find((p) => {
      const time = new Date(p.time);
      if (time.getTime() > now.getTime()) {
        timeLeft = Math.floor((time.getTime() - now.getTime()) / (1000 * 60));
        return true;
      }
      return false;
    });

    return { nextPrayer, timeLeft };
  };

  return (
    <main className="flex items-center justify-center p-2 h-screen">
      <div className="flex items-center justify-center flex-col py-10 gap-8 max-w-600">
        {prayers ? (
          <>
            <Header />
            <CurrentPrayer
              currentPrayer={getCurrentPrayer()}
              {...getNextPrayer()}
            />
            <FuturePrayers prayers={prayers} />
          </>
        ) : (
          <div className="w-20 h-20 bg-primary animate-pulse rounded-full"></div>
        )}
      </div>
    </main>
  );
}
