import { Clock } from "lucide-react";
import type { Prayer } from "../../models/prayers.model";

export default function CurrentPrayer({
  currentPrayer,
  nextPrayer,
  timeLeft,
}: {
  currentPrayer: Prayer;
  nextPrayer?: Prayer;
  timeLeft?: number;
}) {
  return (
    <div className="flex flex-col gap-3 border-2 border-white w-full p-5 rounded-2xl">
      <p className="text-sm bg-primary text-background w-fit py-1 px-2 rounded-md">
        Current Prayer
      </p>
      <h1 className="text-4xl font-bold">{currentPrayer.name}</h1>
      {nextPrayer && (
        <p className="flex items-center gap-2 text-gray-400 text-base">
          {nextPrayer.name}, Starts in {timeLeft} mins <Clock size={20} />
        </p>
      )}
    </div>
  );
}
