// import { Link } from "@heroui/link";
// import { Snippet } from "@heroui/snippet";
// import { Code } from "@heroui/code";
// import { button as buttonStyles } from "@heroui/theme";
//
// import { siteConfig } from "@/config/site.ts";
import { title, subtitle } from "@/components/primitives.ts";
// import { GithubIcon } from "@/components/icons.tsx";
import DefaultLayout from "@/layouts/default.tsx";
import Map from "@/components/map.tsx";

export default function IndexPage() {
  return (
      <DefaultLayout>
        <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
          <div className="max-w-xl text-center justify-center">
            <span className={title()}>Find out about &nbsp;</span><br/>
          <span className={title()}>the &nbsp;</span><span className={title({color: "violet"})}>wildfire probability&nbsp;</span>
            <br/>
            <span className={title()}>
                in advance.
            </span>
            <div className={subtitle({class: "mt-4"})}>
                Just type address or coordinates in the search form <br/>or select a location on the map.
            </div>
          </div>

          {/*<div className="flex gap-3">*/}
          {/*  <Link*/}
          {/*    isExternal*/}
          {/*    className={buttonStyles({*/}
          {/*      color: "primary",*/}
          {/*      radius: "full",*/}
          {/*      variant: "shadow",*/}
          {/*    })}*/}
          {/*    href={siteConfig.links.docs}*/}
          {/*  >*/}
          {/*    Documentation*/}
          {/*  </Link>*/}
          {/*  <Link*/}
          {/*    isExternal*/}
          {/*    className={buttonStyles({ variant: "bordered", radius: "full" })}*/}
          {/*    href={siteConfig.links.github}*/}
          {/*  >*/}
          {/*    <GithubIcon size={20} />*/}
          {/*    GitHub*/}
          {/*  </Link>*/}
          {/*</div>*/}

          {/*<div className="mt-8">*/}
          {/*  <Snippet hideCopyButton hideSymbol variant="bordered">*/}
          {/*    <span>*/}
          {/*      Get started by editing{" "}*/}
          {/*      <Code color="primary">pages/index.tsx</Code>*/}
          {/*    </span>*/}
          {/*  </Snippet>*/}
          {/*</div>*/}
        </section>
        <div style={{width: '100%'}}>
          <Map/>
        </div>
      </DefaultLayout>
  );
}
