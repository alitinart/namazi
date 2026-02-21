import type { Prayer } from "../../models/prayers.model";

export default function FuturePrayers({ prayers }: { prayers: Prayer[] }) {
  const day = "Today's";

  return (
    <div className="w-full flex flex-col gap-3">
      <div className="flex justify-between items-center">
        <h1 className="font-medium">{day} Prayers</h1>
        <button className="text-primary rounded-md cursor-pointer">
          Change Date
        </button>
      </div>
      <div className="flex flex-col gap-4">
        {prayers.map((p) => {
          return <Prayer key={p.name} {...p} />;
        })}
      </div>
    </div>
  );
}

function Prayer(p: Prayer) {
  const date = new Date(p.time);
  const finished = new Date() > date;

  return (
    <div className="grid grid-cols-3 bg-card py-2 px-4 rounded-xl backdrop-blur-2xl w-full justify-between items-center">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-background border-2 border-gray-700 rounded-full flex justify-center items-center">
          {finished && <div className="w-4 h-4 bg-primary rounded-full"></div>}
        </div>
        <p className="font-medium">{p.name}</p>
      </div>
      <p className="font-medium text-center">
        {date.toLocaleTimeString("default", {
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        })}
      </p>
      <p className="text-gray-400 text-end">
        {finished ? "Completed" : "Upcoming"}
      </p>
    </div>
  );
}
