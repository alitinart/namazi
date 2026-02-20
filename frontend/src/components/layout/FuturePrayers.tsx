export default function FuturePrayers() {
  const prayers = [
    { name: "Fajr", finished: true },
    { name: "Dhuhr", finished: false },
    { name: "Magrib", finished: false },
    { name: "Isha", finished: false },
  ];
  const day = "Today's";

  return (
    <div className="w-full flex flex-col gap-3">
      <h1 className="font-medium">{day} Prayers</h1>
      <div className="flex flex-col gap-4">
        {prayers.map((prayer) => {
          return <Prayer key={prayer.name} {...prayer} />;
        })}
      </div>
    </div>
  );
}

function Prayer({ name, finished }: { name: string; finished: boolean }) {
  return (
    <div className="grid grid-cols-3 bg-card py-2 px-4 rounded-xl backdrop-blur-2xl w-full justify-between items-center">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-background border-2 border-gray-700 rounded-full flex justify-center items-center">
          {finished && <div className="w-4 h-4 bg-primary rounded-full"></div>}
        </div>
        <p className="font-medium">{name}</p>
      </div>
      <p className="font-medium text-center">5:12 AM</p>
      <p className="text-gray-400 text-end">
        {finished ? "Completed" : "Upcoming"}
      </p>
    </div>
  );
}
