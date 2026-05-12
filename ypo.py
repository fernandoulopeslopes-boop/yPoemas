import React, { useState } from "react";
import { Eye, Volume2, PocketKnife, Shuffle, RedoDot, ArrowBigLeft, ArrowBigRight, StarNorth, House } from "lucide-react";

const ICON_COLOR = "#c1bad8";
const ICON_SIZE = 20;

const languages = [
  "Português", "Español", "Italiano", "Français", "English",
  "Català", "Deutsch", "Dansk", "Esperanto", "Galego", "Latin",
  "Íslenska", "Nederlands", "Norsk", "Polski", "Portuñol",
  "Română", "Русский", "Svenska", "Suomi", "Magyar"
];

const pages = ["mini", "yPoemas", "eureka", "off-machina", "livros", "poly", "sobre"];

export default function MachinaSidebarPreview() {
  const [page, setPage] = useState("yPoemas");
  const [lang, setLang] = useState("Português");

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex font-sans">
      <aside className="w-[310px] min-h-screen border-r border-zinc-800 bg-zinc-950 flex flex-col px-[5px] py-3">
        <section className="px-1 pb-3">
          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-700 rounded-md px-2 py-1.5 text-[13px] text-[#c1bad8] outline-none"
          >
            {languages.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </section>

        <section className="grid grid-cols-[1fr_1.6fr_1fr] gap-2 px-1 pb-3">
          <button className="h-8 rounded-md border border-zinc-800 bg-zinc-900/60 flex items-center justify-center">
            <Eye size={ICON_SIZE} color={ICON_COLOR} absoluteStrokeWidth />
          </button>
          <button className="h-8 rounded-md border border-zinc-800 bg-zinc-900/60 flex items-center justify-center gap-1 text-[#c1bad8] text-[12px]">
            <PocketKnife size={ICON_SIZE} color={ICON_COLOR} absoluteStrokeWidth />
          </button>
          <button className="h-8 rounded-md border border-zinc-800 bg-zinc-900/60 flex items-center justify-center">
            <Volume2 size={ICON_SIZE} color={ICON_COLOR} absoluteStrokeWidth />
          </button>
        </section>

        <section className="px-1 pb-3">
          <div className="border border-zinc-800 bg-zinc-900/45 rounded-md px-3 py-2 text-[12px] leading-snug text-zinc-300">
            <div className="flex items-center justify-between text-[#c1bad8] mb-1">
              <span>{page}</span>
              <StarNorth size={15} color={ICON_COLOR} absoluteStrokeWidth />
            </div>
            <p>
              info breve da página em foco. texto recolhível depois. aqui só o volume visual.
            </p>
          </div>
        </section>

        <section className="px-1 pb-3">
          <div className="grid grid-cols-5 gap-1">
            <button className="h-7 rounded border border-zinc-800 bg-zinc-900/50 flex items-center justify-center"><ArrowBigLeft size={17} color={ICON_COLOR} absoluteStrokeWidth /></button>
            <button className="h-7 rounded border border-zinc-800 bg-zinc-900/50 flex items-center justify-center"><Shuffle size={17} color={ICON_COLOR} absoluteStrokeWidth /></button>
            <button className="h-7 rounded border border-zinc-800 bg-zinc-900/50 flex items-center justify-center"><RedoDot size={17} color={ICON_COLOR} absoluteStrokeWidth /></button>
            <button className="h-7 rounded border border-zinc-800 bg-zinc-900/50 flex items-center justify-center"><ArrowBigRight size={17} color={ICON_COLOR} absoluteStrokeWidth /></button>
            <button className="h-7 rounded border border-zinc-800 bg-zinc-900/50 flex items-center justify-center"><House size={17} color={ICON_COLOR} absoluteStrokeWidth /></button>
          </div>
        </section>

        <section className="flex-1 px-1 pb-3 min-h-[170px]">
          <div className="h-full rounded-md border border-zinc-800 bg-zinc-900/30 px-3 py-3 text-[13px] leading-snug text-zinc-200 overflow-hidden">
            <div className="text-[#c1bad8] text-[12px] mb-2">mini-palco</div>
            <p>Parece que há pessoas que cultivam pensares plastificados...</p>
            <br />
            <p>Meu dó desse nó é que ele não sabe que dá voltas em torno do próprio só.</p>
          </div>
        </section>

        <section className="px-1 mt-auto">
          <div className="w-[300px] h-[96px] rounded-md overflow-hidden border border-zinc-800 bg-gradient-to-br from-zinc-900 via-violet-950 to-zinc-950 flex items-center justify-center text-[#c1bad8] text-[12px] tracking-wide">
            arte da página • 300 px
          </div>
        </section>
      </aside>

      <main className="flex-1 flex flex-col">
        <nav className="h-12 border-b border-zinc-800 flex items-center px-5 gap-2 bg-zinc-950">
          {pages.map((item) => (
            <button
              key={item}
              onClick={() => setPage(item)}
              className={`px-3 py-1.5 rounded-md text-[13px] ${page === item ? "bg-zinc-800 text-[#c1bad8]" : "text-zinc-500 hover:text-zinc-200"}`}
            >
              {item}
            </button>
          ))}
        </nav>
        <section className="flex-1 flex items-center justify-center text-zinc-700 text-sm">
          palco principal vazio para teste visual da sidebar
        </section>
      </main>
    </div>
  );
}
