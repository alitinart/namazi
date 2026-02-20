import FuturePrayers from "./components/layout/FuturePrayers";
import Header from "./components/layout/Header";
import Prayer from "./components/layout/Prayer";

export default function App() {
  return (
    <main className="flex items-center justify-center">
      <div className="flex items-center justify-center flex-col py-10 gap-8 w-[50%]">
        <Header />
        <Prayer />
        <FuturePrayers />
      </div>
    </main>
  );
}
