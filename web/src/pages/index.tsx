import { title, subtitle } from "@/components/primitives.ts";
import DefaultLayout from "@/layouts/default.tsx";
import Map from "@/components/map.tsx";

export default function IndexPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="max-w-xl text-center justify-center">
          <span className={title()}>Узнайте вероятность &nbsp;</span>
          <br />
          <span className={title({ color: "violet" })}>
            лесного пожара&nbsp;
          </span>
          <span className={title()}>заранее.</span>
          <div className={subtitle({ class: "mt-4" })}>
            Просто введите адрес или координаты в поисковую форму
            или выберите место на карте.
          </div>
        </div>
      </section>
      <div style={{ width: "100%" }}>
        <Map />
      </div>
      <div className="pt-10 pb-10 mx-auto text-center">
        <div>
          © 7 Team <br/>
          { new Date().getFullYear() }
        </div>
      </div>
    </DefaultLayout>
  );
}
