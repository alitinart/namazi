import { Clock } from "lucide-react";

export default function Prayer() {
  return (
    <div className="flex flex-col gap-3 border-2 border-white w-full p-5 rounded-2xl">
      <p className="text-sm bg-primary text-background w-fit py-1 px-2 rounded-md">
        Current Prayer
      </p>
      <h1 className="text-4xl font-bold">Isha</h1>
      <p className="flex gap-2 text-gray-400 text-base">
        Fajr, Starts in 42 mins <Clock />
      </p>
    </div>
  );
}
