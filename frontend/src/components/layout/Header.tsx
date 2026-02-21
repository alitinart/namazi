import { MoonIcon } from "lucide-react";

export default function Header() {
  const date = new Date();

  return (
    <header className="grid grid-cols-[2fr_1fr] gap-10 w-full">
      <div className="flex flex-col justify-center">
        <div>
          <h1 className="font-bold text-xl md:text-2xl">Assalamu Alakeam</h1>
          <p className="text-gray-400">
            {date.toLocaleString("en-US", { weekday: "long" })},{" "}
            {date.toLocaleDateString("default", {
              day: "2-digit",
              month: "short",
            })}
          </p>
        </div>
      </div>
      <div className="flex h-full items-center justify-end">
        <MoonIcon className="h-full w-auto drop-shadow-[0px_3px_20px] drop-shadow-primary" />
      </div>
    </header>
  );
}
