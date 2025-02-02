import { Route, Routes } from "react-router-dom";

import IndexPage from "@/pages";
// import DocsPage from "@/pages/docs.tsx";
import PricingPage from "@/pages/pricing.tsx";
import BlogPage from "@/pages/blog.tsx";
import AboutPage from "@/pages/about.tsx";

function App() {
  return (
    <Routes>
      <Route element={<IndexPage />} path="/" />
      {/*<Route element={<DocsPage />} path="/docs" />*/}
      <Route element={<PricingPage />} path="/pricing" />
      <Route element={<BlogPage />} path="/blog" />
      <Route element={<AboutPage />} path="/about" />
    </Routes>
  );
}

export default App;
