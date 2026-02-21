import { MoonIcon } from "lucide-react";

export default function Header() {
  return (
    <header className="grid grid-cols-[2fr_1fr] gap-10 w-full">
      <div className="flex flex-col justify-center">
        <div>
          <h1 className="font-bold text-xl md:text-2xl">Assalamu Alakeam</h1>
          <p className="text-gray-400">Friday, 20 Feb</p>
        </div>
      </div>
      <div className="flex h-full items-center justify-end">
        <MoonIcon className="h-full w-auto drop-shadow-[0px_3px_20px] drop-shadow-primary" />
      </div>
    </header>
  );
}
